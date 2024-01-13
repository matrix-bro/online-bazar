# Online Bazar

===============

An online marketplace created using Django

Features:

- User Authentication
- Add, Modify and Delete Items
- Search Items using filters
- Chat with Owner
  - Full Chat History

## Run this project locally

===============

1. Clone the repository:

```bash
git clone https://github.com/matrix-bro/online-bazar.git
```

2. Go to project's folder

```bash
cd online-bazar
```

3. Create a virtual environment and activate it

```bash
python -m venv venv

(In windows)
source .\venv\Scripts\activate

(In linux)
source venv/bin/activate
```

4. Install from requirements file

```bash
pip install -r requirements.txt
```

5. Apply migrations

```bash
python manage.py migrate
```

6. Start the development server

```bash
python manage.py runserver
```

### Optional (Create categories using category_dump.json file)

===============

- You can run

```bash
python manage.py loaddata category_dump.json
```

- Or, you can create categories from admin panel.
