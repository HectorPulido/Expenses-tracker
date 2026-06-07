# Expenses Tracker

A simple Django application to track expenses and incomes with interactive visualizations and CSV export.

## Features

* **User Authentication**: Secure login/logout for individual users.
* **Dashboard**: View the last 7 days of expenses and incomes in a table and line chart.
![Dashboard](/images/summary.png)
* **All Records**: Filter records by date range, view a daily summary chart, and generate a weighted word cloud of transaction descriptions.
![Dashboard](/images/stats.png)
* **CSV Export**: Download all records within a chosen date range.
* **Data Visualization**:

  * Line charts powered by Chart.js for temporal trends.
  * Word cloud generated with the Python `wordcloud` library to highlight high-value descriptions.
* **Responsive UI**: Built with Bootstrap 5 and custom CSS.

## Tech Stack

* **Backend**: Python 3.13, Django 4.2+, Django REST Framework
* **Database**: PostgreSQL 16
* **Server**: Gunicorn
* **Frontend**: Bootstrap 5, Chart.js
* **Visualization**: `wordcloud` Python library

---

## Quick start with Docker Compose (recommended)

This is the easiest way to run the project: it starts PostgreSQL and the web app,
runs the migrations, collects the static files and creates an admin user automatically.

### Prerequisites

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/) (included in modern Docker Desktop)

### Steps

1. **Clone the repository and go to the `src` folder** (the `docker-compose.yaml` lives there):

   ```bash
   git clone https://github.com/HectorPulido/Expenses-tracker.git
   cd Expenses-tracker/src
   ```

2. **(Optional) Review the environment variables** in `docker-compose.yaml`.
   The defaults already work for local development — see the table below to know
   what is **important** to change and what is **optional**.

3. **Build and start the containers**:

   ```bash
   docker compose up --build
   ```

4. **Open the app** at [http://localhost:8001](http://localhost:8001).

5. **Log in to the admin** at [http://localhost:8001/admin](http://localhost:8001/admin)
   with the superuser credentials defined in `docker-compose.yaml`
   (by default `admin` / `testpassword`).

To stop the containers press `Ctrl+C`, or run `docker compose down`
(add `-v` to also delete the database volume and start fresh).

### Environment variables

All variables are configured in the `environment:` block of each service in
`docker-compose.yaml`.

#### Important — review/change these

| Variable                    | Service     | Why it matters |
|-----------------------------|-------------|----------------|
| `SECRET_KEY`                | `web`       | Django's cryptographic key. **Must** be a long, unique, random string in production. |
| `POSTGRES_PASSWORD`         | `db` + `web`| Database password. Change it from `changeme`, and keep it **identical in both services** or the app won't connect. |
| `DJANGO_SUPERUSER_USERNAME` | `web`       | Username of the auto-created admin account (used to log in). |
| `DJANGO_SUPERUSER_PASSWORD` | `web`       | Password of the auto-created admin account. Change it from the default. |
| `DJANGO_SUPERUSER_EMAIL`    | `web`       | Email of the auto-created admin account. |
| `ALLOWED_HOSTS`             | `web`       | Comma-separated list of domains/IPs allowed to serve the app. **Add your real domain when deploying** (e.g. `mydomain.com`). See the note below. |

> If you also change `POSTGRES_DB` or `POSTGRES_USER`, remember they must match
> between the `db` and `web` services too.

#### Optional — defaults are fine for local use

| Variable               | Service     | Default       | Notes |
|------------------------|-------------|---------------|-------|
| `DEBUG`                | `web`       | `"True"`      | Set to `"False"` in production. Must be a quoted string in YAML. |
| `ALLOWED_HOSTS`        | `web`       | `localhost,127.0.0.1,0.0.0.0` | Fine for local dev; only needs changing when you deploy to a domain. |
| `POSTGRES_DB`          | `db` + `web`| `expensesdb`  | Database name. |
| `POSTGRES_USER`        | `db` + `web`| `expensesuser`| Database user. |
| `POSTGRES_HOST`        | `web`       | `db`          | **Keep as `db`** — it's the name of the database service in Compose. |
| `POSTGRES_PORT`        | `db` + `web`| `5432`        | PostgreSQL port (internal to the Compose network). |
| `ports` (`web`)        | `web`       | `8001:8000`   | Host port mapping. Change the left side (`8001`) if that port is already in use. |
| `platform`             | `web`       | `linux/amd64` | Forces the amd64 image. On Apple Silicon / ARM you can remove this line to avoid slow emulation. |

### About the `Invalid HTTP_HOST header` error

If you ever see:

```
Invalid HTTP_HOST header: 'localhost:8001'. You may need to add 'localhost' to ALLOWED_HOSTS.
```

it means the host you are using is not in `ALLOWED_HOSTS`. This project now reads
`ALLOWED_HOSTS` from the environment as a **comma-separated list**, with sensible
local defaults (`localhost`, `127.0.0.1`, `0.0.0.0`). To fix the error:

* **Local development**: the defaults already cover it. If you use a different
  host, add it, e.g. `ALLOWED_HOSTS: "localhost,127.0.0.1,myhost.local"`.
* **Deploying to a domain**: add your domain, e.g.
  `ALLOWED_HOSTS: "mydomain.com,www.mydomain.com"`.
* **Quick test / allow everything** (not recommended for production):
  `ALLOWED_HOSTS: "*"`.

> The port (`:8001`) is **not** part of the host for `ALLOWED_HOSTS`, so listing
> `localhost` is enough — you don't need `localhost:8001`.

For CSRF-protected forms behind a custom domain or HTTPS, you may also need to set
`CSRF_TRUSTED_ORIGINS` (comma-separated, **with scheme**), e.g.
`CSRF_TRUSTED_ORIGINS: "https://mydomain.com"`.

---

## Manual installation (without Docker)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/HectorPulido/Expenses-tracker.git
   cd Expenses-tracker/src
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** inside `src/` with at least the following variables
   (you need a running PostgreSQL instance):

   ```ini
   DEBUG=True
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=localhost,127.0.0.1
   POSTGRES_DB=your_db_name
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

5. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Collect static files**:

   ```bash
   python manage.py collectstatic
   ```

7. **Create an admin user**:

   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

9. **Access the application** at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

   > Note: in this manual mode the app runs on port **8000** (Django's `runserver`
   > default). The port **8001** mentioned earlier only applies to Docker Compose,
   > because of the `8001:8000` port mapping.

## Configuration

* Settings are read from environment variables (or a `.env` file) in
  `expenses_tracker/settings.py`: `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`,
  `CSRF_TRUSTED_ORIGINS` and the `POSTGRES_*` database variables.
* Charts and word clouds can be customized in:

  * `tracking/views.py` for data aggregation logic.
  * Templates under `tracking/templates/expenses/` for chart options and styling.

## Usage

1. **Register or log in** at `/login/`.
2. **Dashboard** (`/`) to add new entries and view the last 7 days.
3. **All Records** (`/see_all/`) to filter by date, view statistics, charts, and the word cloud.
4. **Export CSV** via the download button on the All Records page.

## Running Tests

```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


<div align="center">
<h3 align="center">Let's connect 😋</h3>
</div>
<p align="center">
<a href="https://www.linkedin.com/in/hector-pulido-17547369/" target="blank">
<img align="center" width="30px" alt="Hector's LinkedIn" src="https://www.vectorlogo.zone/logos/linkedin/linkedin-icon.svg"/></a> &nbsp; &nbsp;
<a href="https://twitter.com/Hector_Pulido_" target="blank">
<img align="center" width="30px" alt="Hector's Twitter" src="https://www.vectorlogo.zone/logos/twitter/twitter-official.svg"/></a> &nbsp; &nbsp;
<a href="https://www.twitch.tv/hector_pulido_" target="blank">
<img align="center" width="30px" alt="Hector's Twitch" src="https://www.vectorlogo.zone/logos/twitch/twitch-icon.svg"/></a> &nbsp; &nbsp;
<a href="https://www.youtube.com/channel/UCS_iMeH0P0nsIDPvBaJckOw" target="blank">
<img align="center" width="30px" alt="Hector's Youtube" src="https://www.vectorlogo.zone/logos/youtube/youtube-icon.svg"/></a> &nbsp; &nbsp;
<a href="https://pequesoft.net/" target="blank">
<img align="center" width="30px" alt="Pequesoft website" src="https://github.com/HectorPulido/HectorPulido/blob/master/img/pequesoft-favicon.png?raw=true"/></a> &nbsp; &nbsp;
