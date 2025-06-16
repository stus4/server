from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from .profile import get_current_user_id as get_current_user# якщо в profile.py є get_current_user

import os
from models import Chapter, Work, User
from database import get_db
from schemas import ChapterCreate, ChapterUpdate, ChapterOut, ChapterSchema

router = APIRouter(prefix="/chapters", tags=["Chapters"])
WORKS_DIR = "works"
app = FastAPI()
@router.get("/work/{work_id}", response_model=List[ChapterOut])
def get_chapters_for_work(work_id: UUID, db: Session = Depends(get_db)):
    """Отримання списку розділів твору"""
    return db.query(Chapter).filter(Chapter.work_id == work_id).order_by(Chapter.num).all()


@app.get("/chapters/{chapter_id}", response_model=ChapterOut)
async def get_chapter(chapter_id: UUID, db: Session = Depends(get_db)):
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Зчитуємо текст з файлу
    try:
        with open(chapter.file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        # Можеш обробити помилку, якщо файл не знайдений або інша проблема
        content = ""

    return ChapterOut(
        id=chapter.id,
        title=chapter.title,
        content=content,
        num=chapter.num,
        work_id=chapter.work_id,
    )


WORKS_DIR = "works"
@router.post("/", response_model=ChapterOut, status_code=status.HTTP_201_CREATED)
def create_chapter(
    chapter_data: ChapterCreate,
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user)
):
    # Перевірка прав доступу
    work = db.query(Work).get(chapter_data.work_id)
    if not work or work.author != current_user:
        raise HTTPException(status_code=403, detail="Ви не маєте прав на додавання розділу")

    # Відокремлюємо content
    chapter_dict = chapter_data.dict()
    content = chapter_dict.pop("content")

    # Автоматично визначаємо num (номер розділу)
    last_chapter = db.query(Chapter).filter(Chapter.work_id == chapter_data.work_id).order_by(Chapter.num.desc()).first()
    if last_chapter is None:
        new_num = 1
    else:
        new_num = last_chapter.num + 1

    # Формуємо назву файлу з новим num
    work_folder = os.path.join(WORKS_DIR, str(chapter_data.work_id))
    os.makedirs(work_folder, exist_ok=True)
    filename = f"{new_num}-{chapter_data.title.replace(' ', '_')}.txt"
    filepath = os.path.join(work_folder, filename)

    # Записуємо контент у файл
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    # Оновлюємо дані розділу
    chapter_dict['file_path'] = filepath
    chapter_dict['num'] = new_num  # Встановлюємо автоматично обчислений номер

    # Створюємо розділ
    new_chapter = Chapter(**chapter_dict)
    db.add(new_chapter)
    db.commit()
    db.refresh(new_chapter)

    # Повертаємо Pydantic-модель вручну, щоб включити content
    return ChapterOut(
        id=new_chapter.id,
        title=new_chapter.title,
        content=content,
        num=new_chapter.num,
        work_id=new_chapter.work_id,
    )



@router.put("/{chapter_id}", response_model=ChapterOut)
def update_chapter(
    chapter_id: UUID,
    chapter_data: ChapterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Редагування розділу (автором)"""
    chapter = db.query(Chapter).get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Розділ не знайдено")

    work = db.query(Work).get(chapter.work_id)
    if work.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ви не маєте прав на редагування")

    for key, value in chapter_data.dict(exclude_unset=True).items():
        setattr(chapter, key, value)

    db.commit()
    db.refresh(chapter)
    return chapter


@router.delete("/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chapter(
    chapter_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Видалення розділу (автором)"""
    chapter = db.query(Chapter).get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Розділ не знайдено")

    work = db.query(Work).get(chapter.work_id)
    if work.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ви не маєте прав на видалення")

    db.delete(chapter)
    db.commit()
    return
@router.post("/draft", response_model=ChapterOut, status_code=status.HTTP_201_CREATED)
def save_draft(
    chapter_data: ChapterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    work = db.query(Work).get(chapter_data.work_id)
    if not work or work.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ви не маєте прав на додавання розділу")

    new_chapter = Chapter(
        **chapter_data.dict(),
        is_draft=True
    )
    db.add(new_chapter)
    db.commit()
    db.refresh(new_chapter)
    return new_chapter
