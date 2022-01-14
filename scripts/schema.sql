USE main;
CREATE TABLE Persons (
    PersonID int NOT NULL,
    LastName varchar(255) NOT NULL,
    PRIMARY KEY (PersonID)
);

CREATE TABLE Products (
    ProductID int NOT NULL,
    ProductName varchar(255) NOT NULL,
    Price int NOT NULL,
    PRIMARY KEY (ProductID)
);

CREATE TABLE Carts (
    PersonID int NOT NULL,
    ProductID int NOT NULL,
    FOREIGN KEY (PersonID) REFERENCES Persons(PersonID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)

);
