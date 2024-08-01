Start the App:-
fastapi dev main.py


project_root/
│
├── analytics_master/
│   ├── api/
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── sales_router.py
│   │   │   └── category_router.py
│   │   ├── dependencies
│   │   │   ├── __init__.py
│   │   │   ├──repository.py
│   │   │   ├──session.py
│   │   └── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── event.py
│   │   ├── base.py
│   ├── models/
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── BrandData.py
│   │   │   └── CategoryDetails.py
│   │   │   ├── CategoryShareData.py
│   │   │   └── ProductCategoryMapping.py
│   │   │   ├── ProductDetails.py
│   │   │   └── SalesData.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   ├──base.py
│   │   │   ├──CategoryShareResponse.py
│   │   │   └──SalesResponse.py
│   │   └── __init__.py
│   ├── repository/
│   │   ├── crud/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── categoryShare.py
│   │   │   ├── productDetails.py
│   │   │   └── sale.py
│   │   │
│   │   ├──database.py
│   │   ├──event.py
│   │   ├──repository.py
│   │   ├── session.py
│   │   ├── tables.py
│   │   └── __init__.py
│   └── utils/
│       ├── exceptions/
│       │   ├── __init__.py
│       │   ├── database.py
│       │   │
│       │   └── http/
│       │       ├── __init__.py
│       │       └── exc_4xx.py
│       │
│       ├── __init__.py
│       └── load_csv.py
│       
├── main.py
└── requirements.txt