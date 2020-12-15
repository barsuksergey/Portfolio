alter table customers
add constraint PK_CustomerID primary key (CustomerID);

alter table Orders
add constraint PK_OrderID primary key (OrderID);

create nonclustered index IX_CustomerID
on Orders(CustomerID);

create nonclustered index IX_Country
on Customers(Country);

create nonclustered index IX_CompanyName
on Customers(CompanyName);