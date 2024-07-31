# Database Design

### Hotel

|     Column     | Data type |    Note     |
|:--------------:|:---------:|:-----------:|
|       Id       |   CHAR    | Primary Key |
|      Name      |  VARCHAR  |  Not Null   |
|    Location    |  VARCHAR  |  Not Null   |
|    District    |  VARCHAR  |  Not Null   |
|      City      |  VARCHAR  |  Not Null   |
| Classification |    INT    |  Not Null   |
|  Description   |  VARCHAR  |             |

### Room

|  Column  | Data type |    Note     |
|:--------:|:---------:|:-----------:|
|    Id    |   CHAR    | Primary Key |
|    No    |    INT    |  Not Null   |
|  Price   |    INT    |  Not Null   |
|  TypeId  |   CHAR    | Foreign Key |
| Capacity |    INT    |  NOT Null   |
| HotelID  |   CHAR    | Foreign Key |

### Room type

|   Column    | Data type |    Note     |
|:-----------:|:---------:|:-----------:|
|     Id      |   CHAR    | Primary Key |
|    Name     |  VARCHAR  |  Not Null   |
| Description |  VARCHAR  |  Not Null   |

### User

|   Column   | Data type |         Note          |
|:----------:|:---------:|:---------------------:|
|     ID     |   CHAR    |      Primary Key      |
| First name |  VARCHAR  |       Not Null        |
| Last name  |  VARCHAR  |       Not Null        |
|   Email    |  VARCHAR  |       Not Null        |
|  Password  |  VARCHAR  |       Not Null        |
|    Role    |   ENUM    | Guest, manager, admin |

### Hotel manager

|  Column   | Data type |    Note     |
|:---------:|:---------:|:-----------:|
|    Id     |   CHAR    | Primary Key |
| ManagerId |   CHAR    | Foreign Key |
|  HotelId  |   CHAR    | Foreign Key |

### Booking

|       Column       | Data type |                 Note                 |
|:------------------:|:---------:|:------------------------------------:|
|         Id         |   CHAR    |             Primary Key              |
| Expected check in  |   DATE    |               Not Null               |
| Expected check out |   DATE    |               Not Null               |
|      Check in      |   DATE    |                                      |         
|     Check out      |   DATE    |                                      |
|     Base price     |    INT    |               Not Null               |
|    Total price     |    INT    |                                      |
|    Confirmation    |   ENUM    | Pending, canceled,confirmed, refused |
|       UserId       |   CHAR    |             Foreign Key              |
|       RoomId       |   CHAR    |             Foreign Key              |

### Services

|   Column    | Data type |    Note     |
|:-----------:|:---------:|:-----------:|
|     Id      |   CHAR    | Primary Key |
|    Name     |  VARCHAR  |  Not Null   |
| Description |  VARCHAR  |  Not Null   |
|    Price    |    INT    |  Not Null   |
|   HotelId   |   CHAR    | Foreign Key |

### ChosenServices

|  Column   | Data type |    Note     |
|:---------:|:---------:|:-----------:|
|    Id     |   CHAR    | Primary Key |
| ServiceId |   CHAR    | Foreign Key |
| BookingId |   CHAR    | Foreign Key |

### Review

| Column  | Data type |    Note     |
|:-------:|:---------:|:-----------:|
|   Id    |   CHAR    | Primary Key |
|  Star   |    INT    |  Not Null   |
|  Title  |  VARCHAR  |             |
| Comment |  VARCHAR  |             |
| UserId  |   CHAR    | Foreign Key |
| RoomId  |   CHAR    | Foreign Key |

### Voucher

|  Column  | Data type |    Note     |
|:--------:|:---------:|:-----------:|
|    Id    |   CHAR    | Primary Key |
| Discount |    INT    |  Not Null   |
| HotelId  |   CHAR    | Foreign Key |

### ChosenVoucher

|  Column   | Data type |    Note     |
|:---------:|:---------:|:-----------:|
|    Id     |   CHAR    | Primary Key |
| VoucherId |   CHAR    | Foreign Key |
| BookingId |   CHAR    | Foreign Key |

### HotelImage

|   Column   | Data type |    Note     |
|:----------:|:---------:|:-----------:|
|     Id     |   CHAR    | Primary Key |
| Image path |  VARCHAR  |  Not Null   |
|  HotelId   |   CHAR    | Foreign Key |

### RoomImage

|   Column   | Data type |    Note     |
|:----------:|:---------:|:-----------:|
|     Id     |   CHAR    | Primary Key |
| Image path |  VARCHAR  |  Not Null   |
|   RoomId   |   CHAR    | Foreign Key |

### ReviewImage

|   Column   | Data type |    Note     |
|:----------:|:---------:|:-----------:|
|     Id     |   CHAR    | Primary Key |
| Image path |  VARCHAR  |  Not Null   |
|   UserId   |   CHAR    | Foreign Key |
