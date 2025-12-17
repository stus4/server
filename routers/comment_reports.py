# routers/comment_reports.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .user_profile import get_current_user_id as get_current_user
from database import get_db
from models import CommentReport, User, Comment
from schemas import CommentReportCreate, CommentReportResponse

router = APIRouter(
    prefix="/comment-reports",
    tags=["Comment Reports"]
)
@router.post("/", response_model=CommentReportResponse)
def create_comment_report(
    data: CommentReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.query(Comment).filter(Comment.id == data.comment_id).first()

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    report = CommentReport(
        comment_id=data.comment_id,
        user_id=current_user,
        reason=data.reason
    )

    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@router.get("/", response_model=list[CommentReportResponse])
def get_all_comment_reports(db: Session = Depends(get_db)):
    return db.query(CommentReport).order_by(CommentReport.created_at.desc()).all()
@router.get("/comment/{comment_id}", response_model=list[CommentReportResponse])
def get_reports_for_comment(comment_id: int, db: Session = Depends(get_db)):
    return (
        db.query(CommentReport)
        .filter(CommentReport.comment_id == comment_id)
        .all()
    )
@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(CommentReport).filter(CommentReport.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()
