/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: toread
-- ------------------------------------------------------
-- Server version	11.8.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `categories` VALUES
(1,'Фентезі','Магія, вигадані світи, міфічні створіння.'),
(2,'Наукова фантастика','Технології майбутнього, космос, подорожі в часі.'),
(3,'Романтика','Історії кохання, відносин, почуттів.'),
(4,'Драма','Емоційно глибокі сюжети, життєві виклики.'),
(5,'Трилер','Напруженість, інтрига, несподівані повороти.'),
(6,'Жахи','Моторошні історії, надприродні події.'),
(7,'Детектив','Розслідування, загадки, кримінал.'),
(8,'Комедія','Гумористичні сюжети, легкі для читання твори.'),
(9,'Історична проза','Події, засновані на реальній історії.'),
(10,'Містика','Загадкові явища, привиди, містичні таємниці.'),
(11,'Поезія','Вірші, сонети, римовані твори.'),
(12,'Пригоди','Мандрівки, пошуки скарбів, героїчні вчинки.'),
(13,'Антиутопія','Твори про похмурі сценарії майбутнього.'),
(14,'Дитяча література','Твори для молодшої аудиторії.');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `chapters`
--

DROP TABLE IF EXISTS `chapters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `chapters` (
  `id` uuid NOT NULL,
  `work_id` uuid DEFAULT NULL,
  `num` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `file_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_work_num` (`work_id`,`num`),
  CONSTRAINT `chapters_ibfk_1` FOREIGN KEY (`work_id`) REFERENCES `works` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chapters`
--

LOCK TABLES `chapters` WRITE;
/*!40000 ALTER TABLE `chapters` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `chapters` VALUES
('dedd0369-a1da-4ed8-9a24-01667d094c93','9e279e64-aefb-4d56-b3fe-404e73f154b5',0,'string','works/9e279e64-aefb-4d56-b3fe-404e73f154b5/0-string.txt'),
('82c63675-2d4f-421a-a1fa-7c8fb7d7fd6d','1aeddea6-943e-44ba-8aa4-ba90e0e02a56',1,'Сонце','works/1aeddea6-943e-44ba-8aa4-ba90e0e02a56/1-gh.txt'),
('dd6afc71-53e1-4396-8a84-8377512d0f22','5a0893eb-0593-446e-85ef-1f66263aa804',1,'1 розділ','works/5a0893eb-0593-446e-85ef-1f66263aa804/1-1_розділ.txt'),
('4f8b2e47-9ee4-46c9-8835-ab9f63127e7a','4c1eff9f-1f46-426d-b168-dfd48ac872a3',1,'розділ','works/4c1eff9f-1f46-426d-b168-dfd48ac872a3/1-розділ.txt'),
('69761874-ebcb-44ed-a51f-b35d1f6e8f42','00b399c6-f400-4e95-9e8f-930912e5ce88',1,'розділ','works/00b399c6-f400-4e95-9e8f-930912e5ce88/1-розділ.txt'),
('d6930b69-33ea-4fae-a803-f1e08886eccb','1aeddea6-943e-44ba-8aa4-ba90e0e02a56',2,'title of chapter','works/1aeddea6-943e-44ba-8aa4-ba90e0e02a56/2-gh342.txt');
/*!40000 ALTER TABLE `chapters` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `comment_reports`
--

DROP TABLE IF EXISTS `comment_reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment_reports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment_id` int(11) NOT NULL,
  `user_id` uuid DEFAULT NULL,
  `reason` text NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `comment_id` (`comment_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `comment_reports_ibfk_1` FOREIGN KEY (`comment_id`) REFERENCES `comments` (`id`) ON DELETE CASCADE,
  CONSTRAINT `comment_reports_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_reports`
--

LOCK TABLES `comment_reports` WRITE;
/*!40000 ALTER TABLE `comment_reports` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `comment_reports` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL,
  `user_id` uuid DEFAULT NULL,
  `chapter_id` uuid DEFAULT NULL,
  `text` text NOT NULL,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `chapter_id` (`chapter_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`chapter_id`) REFERENCES `chapters` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `ratings`
--

DROP TABLE IF EXISTS `ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ratings` (
  `id` int(11) NOT NULL,
  `work_id` uuid DEFAULT NULL,
  `user_id` uuid DEFAULT NULL,
  `rating` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `work_id` (`work_id`),
  KEY `fk_ratings_user` (`user_id`),
  CONSTRAINT `fk_ratings_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`work_id`) REFERENCES `works` (`id`),
  CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratings`
--

LOCK TABLES `ratings` WRITE;
/*!40000 ALTER TABLE `ratings` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `ratings` VALUES
(1,'0ee24a17-2cf0-11f0-8b27-cdf255d11a0f','22cacf03-2cee-11f0-8b27-cdf255d11a0f',4),
(2,'4e31c5c5-2cf0-11f0-8b27-cdf255d11a0f','069b54ee-2c6e-11f0-90af-dc3881ded79a',5);
/*!40000 ALTER TABLE `ratings` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `id` uuid NOT NULL,
  `user_id` uuid DEFAULT NULL,
  `created_at` timestamp NOT NULL,
  `expires_at` timestamp NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `subscriptions`
--

DROP TABLE IF EXISTS `subscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `subscriptions` (
  `id` uuid NOT NULL,
  `work_id` uuid DEFAULT NULL,
  `user_id` uuid DEFAULT NULL,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  KEY `work_id` (`work_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `subscriptions_ibfk_1` FOREIGN KEY (`work_id`) REFERENCES `works` (`id`),
  CONSTRAINT `subscriptions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscriptions`
--

LOCK TABLES `subscriptions` WRITE;
/*!40000 ALTER TABLE `subscriptions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `subscriptions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `tags_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=203 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tags` VALUES
(1,'Тварини, що розмовляють',14,'Магічні або уявні тварини, які можуть говорити'),
(2,'Сила дружби',14,'Взаємна підтримка та допомога між персонажами'),
(3,'Розуміння наших відмінностей',14,'Прийняття різних культур, рас і світоглядів'),
(4,'Тварина з вадою',14,'Тварина з фізичними або психологічними вадами'),
(5,'Подолання труднощів',14,'Персонажі, які долають серйозні перешкоди'),
(6,'Опанування нової навички',14,'Навчання і вдосконалення нових умінь'),
(7,'Вивчаємо нове про родину',14,'Розкриття нових аспектів родинних відносин'),
(8,'Навчитися ділитися',14,'Вміння ділитися з іншими'),
(9,'Вірність',14,'Лояльність і відданість у стосунках'),
(10,'Відданість',14,'Повага і відданість комусь або чомусь'),
(11,'Управління гнівом',14,'Навчання контролювати гнів та інші емоції'),
(12,'Збираємося до школи',14,'Підготовка до навчання і перший день у школі'),
(13,'Сила уяви',14,'Використання фантазії для вирішення проблем'),
(14,'Сила командної роботи',14,'Спільна робота для досягнення мети'),
(15,'Співчуття',14,'Виявлення співчуття до інших людей або тварин'),
(16,'Сміливість',14,'Прояв хоробрості в небезпечних ситуаціях'),
(17,'Хоробрість',14,'Відвага і мужність у складних обставинах'),
(18,'Чесність',14,'Правдивість і відкритість у стосунках'),
(19,'Зростання',14,'Особистісний розвиток і зміни у житті'),
(20,'Переживання втрати',14,'Обробка болю від втрати когось або чогось'),
(21,'Дія відбувається в наш час',4,'Сюжет розгортається у сучасності'),
(22,'Конфлікт походить з міжособистісних стосунків',4,'Основна драма виникає через стосунки між персонажами'),
(23,'Сімейна драма',4,'Сюжет зосереджений на подіях у родині'),
(24,'Дорослішання',4,'Історія про особистий ріст і перехід у доросле життя'),
(25,'Боротьба з психічною хворобою, залежністю та/аб’юзом, прийняття сексуальної орієнтації',4,'Тематика психологічних викликів, прийняття себе та важких життєвих ситуацій'),
(26,'Неоднозначний фінал',4,'Кінцівка, яка залишає відкриті питання'),
(27,'Немає традиційної структури сюжету',4,'Сюжет подається нестандартно або нелінійно'),
(28,'Жодних потойбічних елементів',4,'В історії немає фантастики чи надприродного'),
(29,'Смерть в родині',4,'Сюжет включає втрату члена родини'),
(30,'Шлях героя',1,'Сюжетна структура, де протагоніст вирушає у подорож, зіштовхується з викликами, і зрештою перемагає.'),
(31,'Другорядні завдання',1,'Персонажі виконують додаткові місії, які допомагають у досягненні головної мети.'),
(32,'Події відбуваються в середньовіччі або щось типу того',1,'Антураж, схожий на Європу Середніх віків, часто без сучасних технологій.'),
(33,'Обраний',1,'Головний герой, якому судилося врятувати світ або виконати особливу місію.'),
(34,'Лиходій',1,'Центральний антагоніст із надзвичайними силами або темною магією.'),
(35,'Наставник',1,'Мудрий персонаж, який навчає або веде героя.'),
(36,'Могутні артефакти',1,'Магічні предмети, які надають силу або ключ до сюжету.'),
(37,'Магічні істоти',1,'Фантастичні створіння, як-от дракони, єдинороги, грифони тощо.'),
(38,'Епічні сюжетні лінії з багатьма персонажами',1,'Масштабні історії, де діють багато героїв та їх сюжетні лінії переплітаються.'),
(39,'Високі ставки (Добро проти Зла)',1,'Боротьба між абсолютним добром і абсолютним злом.'),
(40,'Спадкоємець трону',1,'Персонаж, що дізнається про своє королівське походження або бере владу у фіналі.'),
(41,'Найкращі з найкращих',1,'Персонажі, що виділяються своїми здібностями, знаннями або силою.'),
(42,'Несподівані союзники',1,'Колишні вороги чи незнайомці, які приходять на допомогу.'),
(43,'Герой мимоволі',1,'Персонаж, який не прагне пригод, але змушений діяти.'),
(44,'Врятований кавалерією',1,'Неочікуване підкріплення, що рятує головного героя.'),
(45,'Панянка в біді',1,'Персонаж, який потребує порятунку, зазвичай жінка.'),
(46,'Послідовне навчання',1,'Момент, де герой тренується та вдосконалює свої навички.'),
(47,'Сплатити ціну',1,'Перемога вимагає жертви або втрат.'),
(48,'Війна',NULL,''),
(49,'Події відбуваються в колоніальній Америці',NULL,''),
(50,'Поєднання реальних та вигаданих подій',NULL,''),
(51,'Додавання історичних постатей як персонажів',NULL,''),
(52,'Релігійні теми',NULL,''),
(53,'Соціальні та політичні потрясіння',NULL,''),
(54,'Дві часові лінії',NULL,'Одна лінія подій у минулому, інша — в теперішньому'),
(55,'Довготривалі подорожі',NULL,''),
(56,'Яким було життя',NULL,'Демонстрація побуту в історичному обрамленні'),
(57,'Стається дещо таємниче',6,''),
(58,'Прокляті предмети',6,'Від книжок до ляльок і релігійних дрібничок'),
(59,'Монстри',6,''),
(60,'Інопланетяни',6,''),
(61,'Палаючі очі',6,'Зазвичай з’являються в темряві у моменти високої напруги'),
(62,'Люди можуть бути Злом',6,''),
(63,'Погані речі трапляються вночі',6,''),
(64,'Паралізований страхом',6,'Коли персонаж не може рухатися, говорити чи кричати'),
(65,'Антихрист',6,''),
(66,'Культи і релігійні екстремісти',6,'Часто намагаються викликати демона чи антихриста'),
(67,'Назад у темряву',6,''),
(68,'Травматичне минуле',6,''),
(69,'Другорядний персонаж помирає першим',6,''),
(70,'Відрізані кінцівки',6,''),
(71,'Втрата можливості втекти',6,'Коли персонаж спотикається у найневдаліший момент'),
(72,'Впізнавані типажі',6,''),
(73,'Кармічна відплата',6,''),
(74,'Угода з дияволом',6,''),
(75,'Моторошне оточення',6,'Покинуті місця, кладовища, ліси тощо'),
(76,'Нещасливий фінал',6,''),
(77,'Кінець світу',6,''),
(78,'Переможений монстр повертається до життя',6,''),
(79,'Стається дещо таємниче',6,''),
(80,'Прокляті предмети',6,'Від книжок до ляльок і релігійних дрібничок'),
(81,'Монстри',6,''),
(82,'Інопланетяни',6,''),
(83,'Палаючі очі',6,'Зазвичай з’являються в темряві у моменти високої напруги'),
(84,'Люди можуть бути Злом',6,''),
(85,'Погані речі трапляються вночі',6,''),
(86,'Паралізований страхом',6,'Коли персонаж не може рухатися, говорити чи кричати'),
(87,'Антихрист',6,''),
(88,'Культи і релігійні екстремісти',6,'Часто намагаються викликати демона чи антихриста'),
(89,'Назад у темряву',6,''),
(90,'Травматичне минуле',6,''),
(91,'Другорядний персонаж помирає першим',6,''),
(92,'Відрізані кінцівки',6,''),
(93,'Втрата можливості втекти',6,'Коли персонаж спотикається у найневдаліший момент'),
(94,'Впізнавані типажі',6,''),
(95,'Кармічна відплата',6,''),
(96,'Угода з дияволом',6,''),
(97,'Моторошне оточення',6,'Покинуті місця, кладовища, ліси тощо'),
(98,'Нещасливий фінал',6,''),
(99,'Кінець світу',6,''),
(100,'Переможений монстр повертається до життя',6,''),
(101,'Краса тексту важить більше за сюжет',NULL,'Твори, які дають певні емоції чи досвід через форму тексту, а не сюжет'),
(102,'Дитячі спогади',NULL,'Намагання впоратися з дитячими травмами часто трапляється в художній літературі'),
(103,'Події відбуваються у маленькому містечку',NULL,''),
(104,'Головні герої помирають',NULL,''),
(105,'Неблагополучна сім’я',NULL,''),
(106,'Заплутаний сюжет',NULL,''),
(107,'Жертва – неприємна людина',7,''),
(108,'Фальшивий слід',7,'Персонаж, якого ми можемо вважати зловмисником, а це всього лиш відвертання уваги. '),
(109,'Замкнений простір',7,''),
(110,'Алібі',7,''),
(111,'Перехитрити злочинця',7,'Коли протагоніст вигадує геніальний план, щоб змусити злочинця зізнатися'),
(112,'Трофей',7,'Коли вбивця береже доказ, який його викриває'),
(113,'Протагоніст – підозрюваний',7,'Що буде, якщо детектив – перший у списку підозрюваних?'),
(114,'Виправлення помилок минулого',7,'Протагоніст береться за справу, яка прямо чи опосередковано пов’язана з його минулим промахом.'),
(115,'Драматичне відкриття',7,'Коли персонаж замовчує інформацію з певних причин, поки не відкриває її у найбільш драматичний спосіб'),
(116,'Детектив, якого переслідує минуле',7,''),
(117,'Консультування зі злочинцем',7,''),
(118,'Амнезія',7,'Герой не може згадати, хто він, або якусь важливу інформацію щодо справи'),
(119,'Несподіваний фінал',7,''),
(120,'Краса тексту важить більше за сюжет',NULL,'Твори, які дають певні емоції чи досвід через форму тексту, а не сюжет'),
(121,'Дитячі спогади',NULL,'Намагання впоратися з дитячими травмами часто трапляється в художній літературі'),
(122,'Події відбуваються у маленькому містечку',NULL,''),
(123,'Головні герої помирають',NULL,''),
(124,'Неблагополучна сім’я',NULL,''),
(125,'Заплутаний сюжет',NULL,''),
(126,'Жертва – неприємна людина',7,''),
(127,'Фальшивий слід',7,'Персонаж, якого ми можемо вважати зловмисником, а це всього лиш відвертання уваги. '),
(128,'Замкнений простір',7,''),
(129,'Алібі',7,''),
(130,'Перехитрити злочинця',7,'Коли протагоніст вигадує геніальний план, щоб змусити злочинця зізнатися'),
(131,'Трофей',7,'Коли вбивця береже доказ, який його викриває'),
(132,'Протагоніст – підозрюваний',7,'Що буде, якщо детектив – перший у списку підозрюваних?'),
(133,'Виправлення помилок минулого',7,'Протагоніст береться за справу, яка прямо чи опосередковано пов’язана з його минулим промахом.'),
(134,'Драматичне відкриття',7,'Коли персонаж замовчує інформацію з певних причин, поки не відкриває її у найбільш драматичний спосіб'),
(135,'Детектив, якого переслідує минуле',7,''),
(136,'Консультування зі злочинцем',7,''),
(137,'Амнезія',7,'Герой не може згадати, хто він, або якусь важливу інформацію щодо справи'),
(138,'Несподіваний фінал',7,''),
(139,'Щасливий фінал',3,''),
(140,'Любовний трикутник',3,'Троє персонажів, один вибір і неминучі образи'),
(141,'Вимушена близькість',3,'Двоє персонажів, які знаходять кохання, коли змушені проводити час разом'),
(142,'Заборонене кохання',3,''),
(143,'Від ворогів до закоханих',3,'Персонажі починають з ненависті одне до одного. Але кохання перемагає '),
(144,'Фальшиві стосунки',3,'Один персонаж втягує іншого в гру, де той виконує роль його партнера.'),
(145,'Інша жінка / інший чоловік',3,''),
(146,'Нездатний на кохання',3,'Персонаж, зранений настільки, що відмовився від кохання.'),
(147,'Кохання – це відповідь',3,''),
(148,'Чистота і розпусність',3,'Один персонаж – недосвідчений в коханні. Інший – аж занадто досвідчений.'),
(149,'Кохання з першого погляду',3,''),
(150,'Шлюб за розрахунком',3,''),
(151,'Неочікуваний любовний інтерес',3,''),
(152,'Доленосні стосунки',3,'Визначені долею закохані.'),
(153,'Непорозуміння',3,'Конфлікт викликаний простим непорозумінням.'),
(154,'Штучний інтелект',2,''),
(155,'Антиутопія, дистопія',2,'Тоталітарний уряд та постапокаліптичний пекельний ландшафт.'),
(156,'Подорожі в часі',2,''),
(157,'Подорожі в космосі',2,''),
(158,'Інопланетяни',2,''),
(159,'Альтернативні виміри / всесвіти',2,''),
(160,'Нанотехнології',2,''),
(161,'Імпланти',2,'Змінюють людські тіла і надають їм дивовижні здатності'),
(162,'Сила і технології',2,''),
(163,'Кінець людської раси',2,''),
(164,'Годинник цокає',2,''),
(165,'Завантаження людей',2,'Коли існує технологія, яка дозволяє завантажувати людську свідомість'),
(166,'Зміна тіла',2,'Коли персонажі можуть жити в інших тілах.'),
(167,'Армія клонів',2,'Клонування створює армії, що можуть бути використані для зловмисних цілей'),
(168,'Знищення всесвіту',2,''),
(169,'Небезпеки кріосну',2,''),
(170,'Годинник цокає',5,'Перегони з часом'),
(171,'Проблемний протагоніст',5,''),
(172,'Ненадійний оповідач',5,'Ненадійний оповідач часто бреше читачеві або каже напівправду.'),
(173,'Несподіваний фінал',5,''),
(174,'Нездоланні випробування',5,''),
(175,'Високі ставки',5,''),
(176,'Екзотичні локації',5,''),
(177,'Кліфгенгер',5,''),
(178,'Зниклі діти або чоловік/дружина',5,''),
(179,'Газлайтинг',5,''),
(180,'Сталкер',5,'Історії, де персонаж несе загрозу, спостерігаючи за іншими'),
(181,'Підстава',5,'Часто протагоніст підозрюваний у злочині, який не скоював'),
(182,'Злочин у родині',5,'Коли хтось близьких до протагоніста коїть злочин'),
(183,'Годинник цокає',5,'Перегони з часом'),
(184,'Проблемний протагоніст',5,''),
(185,'Ненадійний оповідач',5,'Ненадійний оповідач часто бреше читачеві або каже напівправду.'),
(186,'Несподіваний фінал',5,''),
(187,'Нездоланні випробування',5,''),
(188,'Високі ставки',5,''),
(189,'Екзотичні локації',5,''),
(190,'Кліфгенгер',5,''),
(191,'Зниклі діти або чоловік/дружина',5,''),
(192,'Газлайтинг',5,''),
(193,'Сталкер',5,'Історії, де персонаж несе загрозу, спостерігаючи за іншими'),
(194,'Підстава',5,'Часто протагоніст підозрюваний у злочині, який не скоював'),
(195,'Злочин у родині',5,'Коли хтось близьких до протагоніста коїть злочин'),
(196,'Аутсайдер',NULL,''),
(197,'Перше кохання',NULL,''),
(198,'Дорослі, які не можуть допомогти, або взагалі злі',NULL,''),
(199,'Обраний',NULL,'Головний герой, який за пророцтвом має стати спасителем Землі )'),
(200,'Темна родинна таємниця',NULL,''),
(201,'Особливі здібності',NULL,''),
(202,'Зниклі або відсутні батьки',NULL,'');
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `user_interactions`
--

DROP TABLE IF EXISTS `user_interactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_interactions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `work_id` uuid DEFAULT NULL,
  `user_id` uuid DEFAULT NULL,
  `is_saved` tinyint(1) NOT NULL DEFAULT 0,
  `is_liked` tinyint(1) NOT NULL DEFAULT 0,
  `is_viewed` tinyint(1) NOT NULL DEFAULT 0,
  `is_read` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `work_id` (`work_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_interactions_ibfk_1` FOREIGN KEY (`work_id`) REFERENCES `works` (`id`),
  CONSTRAINT `user_interactions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_interactions`
--

LOCK TABLES `user_interactions` WRITE;
/*!40000 ALTER TABLE `user_interactions` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `user_interactions` VALUES
(1,'2a0de755-2cf0-11f0-8b27-cdf255d11a0f','dfe96cd8-8a72-4c12-8800-f689b317edd6',1,1,1,0),
(2,'6fb65691-2c79-11f0-90af-dc3881ded79a','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8',1,1,1,0),
(3,'9e279e64-aefb-4d56-b3fe-404e73f154b5','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8',1,1,1,0),
(4,'2a0de755-2cf0-11f0-8b27-cdf255d11a0f','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8',0,1,1,0),
(5,'0ee24a17-2cf0-11f0-8b27-cdf255d11a0f','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8',0,1,0,0),
(6,'4348b3a8-2cf0-11f0-8b27-cdf255d11a0f','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8',0,1,0,0),
(7,'4e31c5c5-2cf0-11f0-8b27-cdf255d11a0f','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8',0,1,0,0);
/*!40000 ALTER TABLE `user_interactions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` uuid NOT NULL,
  `name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `avatar_path` varchar(150) DEFAULT NULL,
  `birth` int(11) DEFAULT NULL,
  `bio` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `users` VALUES
('ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','jfu','igif','stus44','oksikheina2@gmail.com','$2b$12$6gNC7UKhnt67luELph/3E.u.Xt1uQJ3eOug4KEZpFmtHmXmw1ZPsa',NULL,NULL,2001,NULL),
('61cebaa1-5a89-4d0a-a1d1-811b23b3279f','user22','user','user22','usrer@gmail.com','$2b$12$W/7EZTvSSwF0uamAPqPF4.jUUm0bF3/7xNEJQGcm/zxhQ6gSZ94tO',NULL,NULL,2004,NULL),
('22cacf03-2cee-11f0-8b27-cdf255d11a0f','Оксана','Гейна','oksana','oksana@example.com','hashedpassword','+380991234567','/avatars/oksana.png',2006,'Авторка платформеного роману'),
('3d703ad1-2cee-11f0-8b27-cdf255d11a0f','Оксана','Гейна','oksana33','o3ksana@example.com','hashedpassword','+380991234567','/avatars/oksana.png',2006,'Авторка платформеного роману'),
('069b54ee-2c6e-11f0-90af-dc3881ded79a','Оксана','Гейна','stus4','oksikheina@gmail.com','Oksana 2006','+380980999796','/avatars/oksana.jpg',2006,'к'),
('dfe96cd8-8a72-4c12-8800-f689b317edd6','gb','gfv','user','user@gmail.com','$2b$12$JKtYDQ8k1tqSGEoVEG71kupFWt9SQ1mRRHdUkE2uhmpFU/kL/cTIO',NULL,NULL,1994,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `work_statuses`
--

DROP TABLE IF EXISTS `work_statuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_statuses` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_statuses`
--

LOCK TABLES `work_statuses` WRITE;
/*!40000 ALTER TABLE `work_statuses` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `work_statuses` VALUES
(1,'В процесі'),
(2,'Завершено'),
(3,'Заморожено'),
(4,'Чернетка');
/*!40000 ALTER TABLE `work_statuses` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `work_tags`
--

DROP TABLE IF EXISTS `work_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_tags` (
  `work_id` uuid NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`work_id`,`tag_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `work_tags_ibfk_1` FOREIGN KEY (`work_id`) REFERENCES `works` (`id`),
  CONSTRAINT `work_tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_tags`
--

LOCK TABLES `work_tags` WRITE;
/*!40000 ALTER TABLE `work_tags` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `work_tags` VALUES
('00b399c6-f400-4e95-9e8f-930912e5ce88',5),
('1aeddea6-943e-44ba-8aa4-ba90e0e02a56',5),
('5a0893eb-0593-446e-85ef-1f66263aa804',140);
/*!40000 ALTER TABLE `work_tags` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `works`
--

DROP TABLE IF EXISTS `works`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `works` (
  `id` uuid NOT NULL,
  `title` varchar(100) NOT NULL,
  `author` uuid DEFAULT NULL,
  `description` text DEFAULT NULL,
  `cover_path` varchar(150) DEFAULT NULL,
  `file_path` varchar(150) DEFAULT NULL,
  `created_at` timestamp NOT NULL,
  `updated_at` timestamp NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `age_limit` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `status_id` (`status_id`),
  KEY `category_id` (`category_id`),
  KEY `author` (`author`),
  CONSTRAINT `works_ibfk_1` FOREIGN KEY (`status_id`) REFERENCES `work_statuses` (`id`),
  CONSTRAINT `works_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `works_ibfk_3` FOREIGN KEY (`author`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `works`
--

LOCK TABLES `works` WRITE;
/*!40000 ALTER TABLE `works` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `works` VALUES
('5a0893eb-0593-446e-85ef-1f66263aa804','Мечем і полум\'ям','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','Гарний твір',NULL,NULL,'2025-06-15 15:10:52','2025-06-15 15:10:52',1,NULL,1),
('53736f59-8b1a-44d8-92b8-347a856d5286','ипав','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','ва',NULL,NULL,'2025-06-16 09:32:11','2025-06-16 09:32:11',5,NULL,3),
('9e279e64-aefb-4d56-b3fe-404e73f154b5','Сумний твір ','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','Опис сумного твору, де багато тексту про всяке різне і таке всяке ','string','','2025-06-13 09:51:18','2025-06-15 15:00:06',6,18,NULL),
('f3286df0-8b07-4832-8329-41a6c2b1e3d5','Something cool','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','Many things will happen here',NULL,NULL,'2025-06-15 10:31:10','2025-06-15 10:31:10',7,NULL,1),
('00b399c6-f400-4e95-9e8f-930912e5ce88','Шітска мечів','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','Були мечі, а потім їх не стало. А потім вони з\'явились',NULL,NULL,'2025-06-15 10:46:19','2025-06-15 10:46:19',7,NULL,3),
('1c510334-8add-4f62-b420-983fcdcca281','Кінець','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','Після почтаку була середина, а тоді кінець і не закінчилось',NULL,NULL,'2025-06-15 15:12:05','2025-06-15 15:12:05',3,NULL,3),
('1aeddea6-943e-44ba-8aa4-ba90e0e02a56','ndsh','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','Гарний твір про багато гарного і сумного',NULL,NULL,'2025-06-13 10:35:37','2025-06-13 10:35:37',8,NULL,1),
('0ee24a17-2cf0-11f0-8b27-cdf255d11a0f','Вогонь і Пам’ять','22cacf03-2cee-11f0-8b27-cdf255d11a0f','Історія магічного лицаря, що шукає себе у світі без памʼяті.','','/files/fire_memory','2025-05-12 08:16:10','2025-05-12 08:16:10',1,12,2),
('2a0de755-2cf0-11f0-8b27-cdf255d11a0f','Магія Вогню 2.0','22cacf03-2cee-11f0-8b27-cdf255d11a0f','Драматична історія про боротьбу магів у світі, де магія — це найбільша сила.','','/files/magic_fire','2025-05-12 08:16:56','2025-05-12 08:16:56',1,18,2),
('2c045ce7-2cf0-11f0-8b27-cdf255d11a0f','Магія Вогню','22cacf03-2cee-11f0-8b27-cdf255d11a0f','Драматична історія про боротьбу магів у світі, де магія — це найбільша сила.','','/files/magic_fire','2025-05-12 08:16:59','2025-05-12 08:16:59',1,18,2),
('4348b3a8-2cf0-11f0-8b27-cdf255d11a0f','Тінь','22cacf03-2cee-11f0-8b27-cdf255d11a0f','Сумна і загадкова історія про невидиму силу, що переслідує героя через все його життя.','','/files/ghost_shadow','2025-05-12 08:17:38','2025-05-12 08:17:38',2,16,1),
('4e31c5c5-2cf0-11f0-8b27-cdf255d11a0f','Загублені Міста','22cacf03-2cee-11f0-8b27-cdf255d11a0f','Містичні руїни та таємниці загублених цивілізацій, що приховують важливі підказки для майбутнього.','','/files/lost_cities','2025-05-12 08:17:56','2025-05-12 08:17:56',3,12,2),
('58f7be17-2cf0-11f0-8b27-cdf255d11a0f','Танок Легенд','22cacf03-2cee-11f0-8b27-cdf255d11a0f','Епічна сага про стародавніх героїв, чия історія набула міфічного статусу серед нащадків.','','/files/legend_dance','2025-05-12 08:18:14','2025-05-12 08:18:14',1,14,1),
('b7e2ec8c-0024-4141-aaae-d2fa414ef59d','Початок','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','На початку починали.',NULL,NULL,'2025-06-13 14:27:09','2025-06-13 14:27:09',8,NULL,2),
('0b1e2571-b7cb-44b0-97e0-d32b59672676','string','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','string','string','string','2025-06-13 10:13:50','2025-06-13 10:13:50',1,10,1),
('134adfac-1fba-4b8b-8b88-d43d93e30156','Середина кінця','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','А потім було світло',NULL,NULL,'2025-06-15 16:13:28','2025-06-15 16:13:28',7,NULL,2),
('6fb65691-2c79-11f0-90af-dc3881ded79a','Назва твору 1','069b54ee-2c6e-11f0-90af-dc3881ded79a','Опис твору 1','','/files/work1/','2025-05-09 11:26:42','2025-05-09 11:26:42',1,12,1),
('6fb65b19-2c79-11f0-90af-dc3881ded79a','Назва твору 2','069b54ee-2c6e-11f0-90af-dc3881ded79a','Опис твору 2','','/files/k','2025-05-09 11:26:42','2025-05-09 11:26:42',2,16,2),
('4c1eff9f-1f46-426d-b168-dfd48ac872a3','приатві','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','рч',NULL,NULL,'2025-06-16 09:30:44','2025-06-16 09:30:44',6,NULL,3),
('65f352cb-31c5-4441-86fd-f552bda0f436','Розпочати роботу','ec4fb74a-56a9-4355-94a6-7d6f10ea2ae8','Робота розпочалась а потім був відпочинок',NULL,NULL,'2025-06-13 14:41:30','2025-06-13 14:41:30',7,NULL,2);
/*!40000 ALTER TABLE `works` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-06-21 15:27:41
