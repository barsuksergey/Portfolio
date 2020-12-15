select Categories.CategoryName, count(Products.ProductName) as [Number of Products] from Products
inner join Categories on Categories.CategoryID = Products.CategoryID
group by Categories.CategoryName;

select LastName, FirstName, Region from Employees
Where Region is not null;

select Reg.RegionDescription, Count(Distinct Emp.EmployeeID) from EmployeeTerritories EmpTer
inner join Employees Emp on Emp.EmployeeID = EmpTer.EmployeeID
inner join Territories Ter on EmpTer.TerritoryID = Ter.TerritoryID
inner join Region Reg on Ter.RegionID = Reg.RegionID
Group by Reg.RegionDescription;

select ProductName, UnitsInStock from Products
where UnitsInStock = (select max(unitsinstock) from products);

Select Prod.ProductName, OrdDet.Quantity, Ord.OrderID, Ord.OrderDate, Cust.CompanyName from Customers Cust
inner join Orders Ord on Cust.CustomerID = Ord.CustomerID
inner join [Order Details] OrdDet on OrdDet.OrderID = Ord.OrderID
inner join Products Prod on OrdDet.ProductID = Prod.ProductID
order by Ord.OrderID, Prod.ProductName;

drop index Employees.LastName;
drop index Employees.PostalCode;

create index City on Employees(city);