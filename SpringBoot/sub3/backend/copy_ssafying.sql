drop database ssafying; create database ssafying; use ssafying; 
 CREATE TABLE `Article` ( `articleId` int auto_increment primary key NOT NULL, `userId` varchar(32) NOT NULL, `title` varchar(100) NOT NULL, `content` longtext NOT NULL, `mainCategory` varchar(30) NOT NULL, `subCategory` varchar(30) NOT NULL, `price` int NULL, `location` varchar(10) NULL, `articleImage` varchar(100) NULL, `watchCount` int NOT NULL DEFAULT 0, `createdAt` datetime NOT NULL DEFAULT current_timestamp(), `updatedAt` datetime NOT NULL DEFAULT current_timestamp() );
 CREATE TABLE `User` ( `userId` varchar(32) primary key NOT NULL, `email` varchar(100) unique NOT NULL, `password` varchar(100) NOT NULL, `nickname` varchar(30) unique NOT NULL, `username` varchar(30) NOT NULL, `birthday` date NOT NULL, `grade` int NOT NULL, `profileImage` varchar(100) NULL, `createdAt` datetime NOT NULL DEFAULT current_timestamp(), `gender` varchar(10) NULL, `report` int NOT NULL DEFAULT 0, `isActive` int NOT NULL DEFAULT 0, `role` varchar(20) NULL );
 CREATE TABLE `ArticleLike` ( `articlelikeId` int auto_increment primary key NOT NULL, `userId` varchar(32) NOT NULL, `articleId` int NOT NULL );
 CREATE TABLE `Comment` ( `commentId` int auto_increment primary key NOT NULL, `articleId` int NOT NULL, `userId` varchar(32) NOT NULL, `content` varchar(200) NOT NULL, `createdAt` datetime NOT NULL DEFAULT current_timestamp(), `updatedAt` datetime NOT NULL DEFAULT current_timestamp(), `parentId` int NULL );
 CREATE TABLE `CommentLike` ( `commentLikeId` int auto_increment primary key NOT NULL, `userId` varchar(32) NOT NULL, `commentId` int NOT NULL );
 CREATE TABLE `ArticleAlert` ( `articleAlertId` int auto_increment primary key NOT NULL, `userId` varchar(32) NOT NULL, `articleId` int NULL, `title` varchar(100) NULL, `createdAt` datetime NOT NULL DEFAULT current_timestamp(), `isRead` int NOT NULL DEFAULT 0 );
 CREATE TABLE `ChatRoom` ( `chatRoomId` varchar(32) primary key NOT NULL, `createdAt` datetime NOT NULL DEFAULT current_timestamp(), `type` varchar(100) NOT NULL, `name` varchar(100) unique NOT NULL, `content` varchar(200) NULL, `isLock` int NOT NULL DEFAULT 0, `hostId` varchar(32) NULL );
 CREATE TABLE `Message` ( `messageId` int auto_increment primary key NOT NULL, `title` varchar(100) NOT NULL, `content` varchar(100) NOT NULL, `createAt` datetime NOT NULL DEFAULT current_timestamp(), `isRead` int NOT NULL DEFAULT 0, `userId` varchar(32) NOT NULL, `userId2` varchar(32) NOT NULL );
 CREATE TABLE `WaitUser` ( `userId` varchar(32) primary key NOT NULL, `email` varchar(100) unique NOT NULL, `password` varchar(100) NOT NULL, `nickname` varchar(100) unique NULL, `username` varchar(100) NOT NULL, `birthday` date NOT NULL, `grade` int NOT NULL, `profileImage` varchar(100) NOT NULL, `createdAt` datetime NULL DEFAULT current_timestamp(), `sex` char(1) NULL, `report` int NOT NULL DEFAULT 0 );
 CREATE TABLE `ChatGroup` ( `chatGroupId` int auto_increment primary key NOT NULL, `chatGroupName` varchar(100) NOT NULL, `createdAt` datetime NOT NULL DEFAULT current_timestamp(), `isActive` int NOT NULL DEFAULT 0 );
 CREATE TABLE `ChatMessage` ( `chatId` int auto_increment primary key NOT NULL, `messageBody` text NOT NULL, `createdAt` datetime NOT NULL DEFAULT current_timestamp(), `parentId` int NULL, `userId` varchar(32) NOT NULL );
 CREATE TABLE `Reception` ( `receptionId` int auto_increment primary key NOT NULL, `isRead` int NOT NULL DEFAULT 0, `chatId` int NOT NULL, `userId` varchar(32) NULL, `chatJoinId` int NULL );
 CREATE TABLE `ChatJoin` ( `chatJoinId` int auto_increment primary key NOT NULL, `createDate` datetime NOT NULL DEFAULT current_timestamp(), `isActive` int NOT NULL DEFAULT 0, `chatGroupId` int NOT NULL, `userId` varchar(32) NOT NULL );
 CREATE TABLE `Follow` ( `followId` int auto_increment primary key NOT NULL, `followerId` varchar(32) NOT NULL, `followingId` varchar(32) NOT NULL );
 CREATE TABLE `Chat` ( `chatId` int auto_increment primary key NOT NULL, `chatRoomId` varchar(32) NOT NULL, `createdAt` datetime NOT NULL DEFAULT current_timestamp(), `content` varchar(100) NOT NULL, `userId` varchar(32) NOT NULL, `nickname` varchar(30) NOT NULL );
 CREATE TABLE `Enroll` ( `enrollId` int auto_increment primary key NOT NULL, `createdAt` datetime NOT NULL DEFAULT current_timestamp(), `chatRoomId` varchar(32) NOT NULL, `userId` varchar(32) NOT NULL, `isHost` int NOT NULL );
 CREATE TABLE `EnrollAlert` ( `enrollAlertId` int auto_increment primary key NOT NULL, `createdAt` datetime NOT NULL DEFAULT current_timestamp(), `isRead` int NOT NULL DEFAULT 0, `userId` varchar(32) NOT NULL, `nickname` varchar(100) NOT NULL, `chatRoomId` varchar(32) NOT NULL, `name` varchar(100) NOT NULL, `hostId` varchar(32) NOT NULL );
 CREATE TABLE `InviteAlert` ( `inviteAlertId` int auto_increment primary key NOT NULL, `createdAt` datetime NOT NULL DEFAULT current_timestamp(), `isRead` int NOT NULL DEFAULT 0, `hostId` varchar(32) NOT NULL, `nickname` varchar(100) NOT NULL, `chatRoomId` varchar(32) NOT NULL, `name` varchar(100) NOT NULL, `userId` varchar(32) NOT NULL );
 ALTER TABLE `Article` ADD CONSTRAINT `FK_User_TO_Article_1` FOREIGN KEY ( `userId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `ArticleLike` ADD CONSTRAINT `FK_User_TO_ArticleLike_1` FOREIGN KEY ( `userId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `ArticleLike` ADD CONSTRAINT `FK_Article_TO_ArticleLike_1` FOREIGN KEY ( `articleId` ) REFERENCES `Article` ( `articleId` ) ON DELETE CASCADE;
 ALTER TABLE `Comment` ADD CONSTRAINT `FK_Article_TO_Comment_1` FOREIGN KEY ( `articleId` ) REFERENCES `Article` ( `articleId` ) ON DELETE CASCADE;
 ALTER TABLE `Comment` ADD CONSTRAINT `FK_User_TO_Comment_1` FOREIGN KEY ( `userId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `Comment` ADD CONSTRAINT `FK_Comment_TO_Comment_1` FOREIGN KEY ( `parentId` ) REFERENCES `Comment` ( `commentId` ) ON DELETE CASCADE;
 ALTER TABLE `CommentLike` ADD CONSTRAINT `FK_User_TO_CommentLike_1` FOREIGN KEY ( `userId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `CommentLike` ADD CONSTRAINT `FK_Comment_TO_CommentLike_1` FOREIGN KEY ( `commentId` ) REFERENCES `Comment` ( `commentId` ) ON DELETE CASCADE;
 ALTER TABLE `ArticleAlert` ADD CONSTRAINT `FK_User_TO_ArticleAlert_1` FOREIGN KEY ( `userId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `ArticleAlert` ADD CONSTRAINT `FK_Article_TO_ArticleAlert_1` FOREIGN KEY ( `articleId` ) REFERENCES `Article` ( `articleId` ) ON DELETE CASCADE;
 ALTER TABLE `Message` ADD CONSTRAINT `FK_User_TO_Message_1` FOREIGN KEY ( `userId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `Message` ADD CONSTRAINT `FK_User_TO_Message_2` FOREIGN KEY ( `userId2` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `ChatMessage` ADD CONSTRAINT `FK_ChatMessage_TO_ChatMessage_1` FOREIGN KEY ( `parentId` ) REFERENCES `ChatMessage` ( `chatId` ) ON DELETE CASCADE;
 ALTER TABLE `ChatMessage` ADD CONSTRAINT `FK_User_TO_ChatMessage_1` FOREIGN KEY ( `userId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `Reception` ADD CONSTRAINT `FK_ChatMessage_TO_Reception_1` FOREIGN KEY ( `chatId` ) REFERENCES `ChatMessage` ( `chatId` ) ON DELETE CASCADE;
 ALTER TABLE `Reception` ADD CONSTRAINT `FK_User_TO_Reception_1` FOREIGN KEY ( `userId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `Reception` ADD CONSTRAINT `FK_ChatJoin_TO_Reception_1` FOREIGN KEY ( `chatJoinId` ) REFERENCES `ChatJoin` ( `chatJoinId` ) ON DELETE CASCADE;
 ALTER TABLE `ChatJoin` ADD CONSTRAINT `FK_ChatGroup_TO_ChatJoin_1` FOREIGN KEY ( `chatGroupId` ) REFERENCES `ChatGroup` ( `chatGroupId` ) ON DELETE CASCADE;
 ALTER TABLE `ChatJoin` ADD CONSTRAINT `FK_User_TO_ChatJoin_1` FOREIGN KEY ( `userId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `Follow` ADD CONSTRAINT `FK_User_TO_Follow_1` FOREIGN KEY ( `followerId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `Follow` ADD CONSTRAINT `FK_User_TO_Follow_2` FOREIGN KEY ( `followingId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `Chat` ADD CONSTRAINT `FK_ChatRoom_TO_Chat_1` FOREIGN KEY ( `chatRoomId` ) REFERENCES `ChatRoom` ( `chatRoomId` ) ON DELETE CASCADE;
 ALTER TABLE `Enroll` ADD CONSTRAINT `FK_ChatRoom_TO_Enroll_1` FOREIGN KEY ( `chatRoomId` ) REFERENCES `ChatRoom` ( `chatRoomId` ) ON DELETE CASCADE;
 ALTER TABLE `Enroll` ADD CONSTRAINT `FK_User_TO_Enroll_1` FOREIGN KEY ( `userId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `EnrollAlert` ADD CONSTRAINT `FK_User_TO_EnrollAlert_1` FOREIGN KEY ( `userId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `EnrollAlert` ADD CONSTRAINT `FK_ChatRoom_TO_EnrollAlert_1` FOREIGN KEY ( `chatRoomId` ) REFERENCES `ChatRoom` ( `chatRoomId` ) ON DELETE CASCADE;
 ALTER TABLE `InviteAlert` ADD CONSTRAINT `FK_User_TO_InviteAlert_1` FOREIGN KEY ( `hostId` ) REFERENCES `User` ( `userId` ) ON DELETE CASCADE;
 ALTER TABLE `InviteAlert` ADD CONSTRAINT `FK_ChatRoom_TO_InviteAlert_1` FOREIGN KEY ( `chatRoomId` ) REFERENCES `ChatRoom` ( `chatRoomId` ) ON DELETE CASCADE;

insert into User(userId, email, password, nickname, username, birthday, grade, gender, role) values('00000000000000000000000000000000', 'admin@ssafying.com', '12341234', 'admin', 'admin', '2021-02-17', 0, 'they', 'ROLE_ADMIN');
