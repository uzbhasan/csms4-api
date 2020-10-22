# CSMS4 REST-API
## Starting
Start the virtual environment and install dependencies:
```
pip install -r requirements.txt
```
Delete all migration files, make migrations and migrate:
```
python manage.py makemigrations
python manage.py migrate
```
Create superuser:
```
python manage.py createsuperuser
```

## URLs
- Admin panel: ``127.0.0.1:8000/admin/``
- REST-API: ``127.0.0.1:8000/api/``

## Models and API URLs
1. Company
   - GET: 
      - Get all companies: ``/company/``
      - Retrieve: ``/company/<company_id>``
   - POST:
      - Create a new: ``/company/``
   - PUT:
      - Update: ``/company/<company_id>``
   - DELETE: ``/company/<company_id>``
2. Account
   - GET:
      - Get all accounts: ``/account/``
      - Retrieve: ``/account/<user_id>``
   - POST:
      - Create a new: ``/account/``
   - DELETE:
      - Inactive: ``/account/<user_id>``
      - Force delete: ``/account/delete/<user_id>``
   - PUT:
      - Create/change avatar: ``/change/avatar/<user_id>``
      - Change password: ``/change/password/<user_id>``
      - Restore (activate): ``/restore/<user_id>``
3. Slope
   - GET:
      - Get all slopes: ``/slope/``
      - Retrieve: ``/slope/<id>``
   - POST:
      - Create a new: ``/slope/``
   - PUT:
      - Update: ``/slope/<id>``
   - DELETE:
      - Inactive: ``/slope/<id>``
      - Force delete: ``/slope/delete/<id>``
4. ExpertImage
   - GET:
      - Get all images: ``/expert-image/``
      - Retrieve: ``/expert-image/<id>``
   - POST:
      - Create a new: ``/expert-image/``
   - DELETE:
      - Inactive: ``/expert-image/<id>``
      - Force delete: ``/expert-image/delete/<id>``
5. DModel (_3D models_)
   - GET:
      - Get all models: ``/model/``
      - Retrieve: ``/model/<id>``
   - POST:
      - Create a new: ``/model/``
   - DELETE:
      - Inactive: ``/model/<id>``
      - Force delete: ``/model/delete/<id>``
6. Order
   - GET:
      - Get all orders: ``/order/``
      - Retrieve: ``/order/<id>``
   - POST:
      - Create a new: ``/order/``
   - PUT:
      - Update: ``/order/<id>``
   - DELETE:
      - Inactive: ``/order/<id>``
      - Force delete: ``/order/delete/<id>``
      
7. OrderImage
   - GET:
      - Get all images: ``/order-image/``
      - Retrieve: ``/order-image/<id>``
   - POST:
      - Create a new: ``/order-image/``
   - DELETE:
      - Inactive: ``/order-image/<id>``
      - Force delete: ``/order-image/delete/<id>``