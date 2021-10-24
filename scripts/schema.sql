USE main;
CREATE TABLE Persons (
    PersonID int NOT NULL,
    LastName varchar(255) NOT NULL
);

CREATE TABLE Products (
    ProductID int PRIMARY KEY,
    ProductName varchar(255),
    Price int
);

CREATE TABLE Carts (
    PersonID int ,
    ProductID int,
);
