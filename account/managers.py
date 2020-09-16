from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, role='EM', company=None, password=None):
        """
        Creates and saves a User with the given email, role,
        first_name, last_name, company and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not role:
            raise ValueError('Users must have a role')

        if not first_name:
            raise ValueError('Users must have a first name')

        if not last_name:
            raise ValueError('Users must have a last name')

        if role == 'SA' and company is not None:
            raise ValueError('System administrators should not have any kind of company')

        if role == 'AD' and company is not None:
            raise ValueError('Administrators should not have any kind of company')

        if role != 'SA' and role != 'AD' and company is None:
            raise ValueError('Company members must have a company')

        user = self.model(
            email=self.normalize_email(email),
            role=role,
            first_name=first_name,
            last_name=last_name,
            company=company
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email,
        first_name, last_name and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            role='SA',
            password=password,
        )
        user.save(using=self._db)
        return user

    def create_administrator(self, email, first_name, last_name, password=None):
        """
        Creates and saves a administrator with the given email,
        first_name, last_name and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            role='AD',
            password=password,
        )
        user.save(using=self._db)
        return user

    def create_general_manager(self, email, first_name, last_name, company, password=None):
        """
        Creates and saves the company's general manager with the given email,
        first_name, last_name, company and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            company=company,
            role='GM',
            password=password,
        )
        user.save(using=self._db)
        return user

    def create_manager(self, email, first_name, last_name, company, password=None):
        """
        Creates and saves the company's manager with the given email,
        first_name, last_name, company and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            company=company,
            role='MA',
            password=password,
        )
        user.save(using=self._db)
        return user

    def create_employee(self, email, first_name, last_name, company, password=None):
        """
        Creates and saves the company's employee with the given email,
        first_name, last_name, company and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            company=company,
            role='EM',
            password=password,
        )
        user.save(using=self._db)
        return user
