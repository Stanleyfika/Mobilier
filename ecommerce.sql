CREATE DATABASE Mobilier ;
USE Mobilier;



CREATE TABLE User (
    IdUser INT AUTO_INCREMENT PRIMARY KEY,
    Pseudo VARCHAR(50) NOT NULL UNIQUE,
    Motdepasse VARCHAR(255) NOT NULL  -- Stockez toujours les mots de passe hashés
);



insert into User(Pseudo,Motdepasse) values('stan','stan');
insert into User(Pseudo,Motdepasse) values('stanley','stan');