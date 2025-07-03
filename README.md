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

* **Backend**: Python, Django 3.1, Django REST Framework
* **Database**: PostgreSQL
* **Frontend**: Bootstrap 5, Chart.js
* **Visualization**: `wordcloud` Python library
* **Internationalization**: `django-babel`

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/tu-usuario/expenses-tracker.git
   cd expenses-tracker/src
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

4. **Create a `.env` file** in the project root with the following variables:

   ```ini
   SECRET_KEY=your-secret-key
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

7. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

8. **Access the application** at `http://127.0.0.1:8000/`.

## Configuration

* Edit `settings.py` or your `.env` file to adjust database settings, `DEBUG` mode, and allowed hosts.
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

---

<div align="center">
<h3 align="center">Let's connect 😋</h3>
</div>
<p align="center">
<a href="https://www.linkedin.com/in/hector-pulido-17547369/" target="blank">
<img align="center" width="30px" alt="Hector's LinkedIn" src="https://github.com/HectorPulido/HectorPulido/blob/master/img/linkedin-icon.svg?raw=true"/></a> &nbsp; &nbsp;
<a href="https://twitter.com/Hector_Pulido_" target="blank">
<img align="center" width="30px" alt="Hector's Twitter" src="https://github.com/HectorPulido/HectorPulido/blob/master/img/twitter-official.svg?raw=true"/></a> &nbsp; &nbsp;
<a href="https://www.twitch.tv/hector_pulido_" target="blank">
<img align="center" width="30px" alt="Hector's Twitch" src="https://github.com/HectorPulido/HectorPulido/blob/master/img/twitch-icon.svg?raw=true"/></a> &nbsp; &nbsp;
<a href="https://www.youtube.com/channel/UCS_iMeH0P0nsIDPvBaJckOw" target="blank">
<img align="center" width="30px" alt="Hector's Youtube" src="https://github.com/HectorPulido/HectorPulido/blob/master/img/youtube-icon.svg?raw=true"/></a> &nbsp; &nbsp;
<a href="https://pequesoft.net/" target="blank">
<img align="center" width="30px" alt="Pequesoft website" src="https://github.com/HectorPulido/HectorPulido/blob/master/img/pequesoft-favicon.png?raw=true"/></a> &nbsp; &nbsp;

</p>
