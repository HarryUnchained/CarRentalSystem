create table dbo.Admin
(
    AdminID     int identity
        primary key,
    Username    varchar(50),
    Password    varchar(100),
    Master      bit default 0 not null,
    PhoneNumber nvarchar(15),
    constraint CHK_PhoneNumber_Format
        check ([Master] = 1 AND [PhoneNumber] IS NOT NULL AND
               ([PhoneNumber] like '+92[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' OR
                [PhoneNumber] like '03[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]') OR
               [Master] = 0 AND [PhoneNumber] IS NULL)
)
go

create table dbo.Brand
(
    BrandID   int identity
        primary key,
    BrandName varchar(50)
)
go

create table dbo.Category
(
    CategoryID   int identity
        primary key,
    CategoryName varchar(50)
)
go

create table dbo.City
(
    CityID   int identity
        primary key,
    CityName varchar(50)
)
go

create table dbo.Branch
(
    BranchID   int identity
        primary key,
    BranchName varchar(100),
    Address    varchar(100),
    CityID     int
        references dbo.City,
    PostalCode varchar(20)
)
go

create table dbo.Color
(
    ColorID   int identity
        primary key,
    ColorName varchar(50)
)
go

create table dbo.Customer
(
    CustomerID int identity
        primary key,
    FirstName  varchar(50),
    LastName   varchar(50),
    Email      varchar(100),
    Phone      varchar(20),
    Address    varchar(100)
)
go

create table dbo.Discount
(
    DiscountID int identity
        primary key,
    Code       varchar(50),
    Percentage decimal(5, 2),
    StartDate  date,
    EndDate    date
)
go

create table dbo.Employee
(
    EmployeeID int identity
        primary key,
    FirstName  varchar(50),
    LastName   varchar(50),
    Email      varchar(100),
    Phone      varchar(20),
    Position   varchar(50)
)
go

create table dbo.Extra
(
    ExtraID     int identity
        primary key,
    ExtraName   varchar(100),
    Description varchar(200),
    Price       decimal(10, 2)
)
go

create table dbo.FuelType
(
    FuelTypeID   int identity
        primary key,
    FuelTypeName varchar(50)
)
go

create table dbo.InsuranceOption
(
    InsuranceOptionID   int identity
        primary key,
    InsuranceOptionName varchar(100),
    Description         varchar(200),
    CoverageAmount      decimal(10, 2)
)
go

create table dbo.Location
(
    LocationID   int identity
        primary key,
    LocationName varchar(100),
    Address      varchar(100),
    CityID       int
        references dbo.City,
    PostalCode   varchar(20)
)
go

create table dbo.Make
(
    MakeID   int identity
        primary key,
    MakeName varchar(50) collate SQL_Latin1_General_CP1_CS_AS
        constraint CK_MakeName_Uppercase
            check ([MakeName] = upper([MakeName]))
)
go

-- Create a trigger to automatically convert MakeName to uppercase
CREATE TRIGGER TR_Make_Uppercase
ON Make
AFTER INSERT, UPDATE
AS
BEGIN
    UPDATE Make
    SET MakeName = UPPER(Make.MakeName)
    FROM Make
    INNER JOIN inserted ON Make.MakeID = inserted.MakeID
END
go

create table dbo.Model
(
    ModelID   int identity
        primary key,
    ModelName varchar(50),
    Year      int
)
go

create table dbo.PaymentMethod
(
    PaymentMethodID   int identity
        primary key,
    PaymentMethodName varchar(50),
    Description       varchar(200)
)
go

create table dbo.RentalDuration
(
    RentalDurationID int identity
        primary key,
    DurationName     varchar(50),
    DurationHours    int
)
go

create table dbo.RentalRate
(
    RentalRateID   int identity
        primary key,
    CarID          int,
    RentalDuration int
        references dbo.RentalDuration,
    Rate           decimal(10, 2)
)
go

create table dbo.Reservation
(
    ReservationID int identity
        primary key,
    CustomerID    int
        references dbo.Customer,
    CarID         int,
    PickupDate    date,
    DropoffDate   date
)
go

create table dbo.Invoice
(
    InvoiceID     int identity
        primary key,
    ReservationID int
        references dbo.Reservation,
    TotalAmount   decimal(10, 2),
    IssuedDate    date,
    DueDate       date,
    PaymentStatus varchar(50)
)
go

create table dbo.RentalAgreement
(
    AgreementID    int identity
        primary key,
    ReservationID  int
        references dbo.Reservation,
    CustomerID     int
        references dbo.Customer,
    AgreementDate  date,
    AgreementTerms varchar(200)
)
go

create table dbo.Review
(
    ReviewID   int identity
        primary key,
    CustomerID int
        references dbo.Customer,
    CarID      int,
    Rating     int,
    Comment    varchar(200)
)
go

create table dbo.[Transaction]
(
    TransactionID   int identity
        primary key,
    ReservationID   int
        references dbo.Reservation,
    Amount          decimal(10, 2),
    TransactionType varchar(50),
    TransactionDate date
)
go

create table dbo.TransmissionType
(
    TransmissionTypeID   int identity
        primary key,
    TransmissionTypeName varchar(50)
)
go

create table dbo.Car
(
    CarID              int identity,
    MakeID             int         not null
        constraint Car_Car__MakeID
            references dbo.Make,
    ModelID            int         not null
        references dbo.Model,
    ColorID            int         not null
        references dbo.Color,
    RegistrationNumber varchar(20) not null
        constraint Car_pk
            primary key nonclustered,
    FuelTypeID         int         not null
        references dbo.FuelType,
    TransmissionTypeID int         not null
        references dbo.TransmissionType
)
go

create table dbo.Availability
(
    AvailabilityID     int identity
        primary key,
    PickupDate         date,
    DropoffDate        date,
    Available          bit default 1 not null,
    RegistrationNumber varchar(20)
        constraint FK_Availability_Cars
            references dbo.Car
)
go

create table dbo.Maintenance
(
    MaintenanceID      int identity
        primary key,
    RegistrationNumber varchar(20)
        constraint Reg_No
            references dbo.Car,
    Description        varchar(200),
    MaintenanceDate    date
)
go

