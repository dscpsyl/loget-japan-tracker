<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/dscpsyl/loget-japan-tracker">
    <img src=".github/logo.png" alt="Logo">
  </a>

<h3 align="center">LoGet Tracker</h3>

  <p align="center">
    A simple tracker for the LoGet collectable cards for tourists in Japan. The official LoGet site is <a href='https://loget-card.jp/'>here</a>.
    <br />
    <br />
    <a href="https://github.com/dscpsyl/loget-japan-tracker">Access the Tracker</a>
    ·
    <a href="https://github.com/dscpsyl/loget-japan-tracker/issues">Report Bug</a>
    ·
    <a href="https://github.com/dscpsyl/loget-japan-tracker/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

![Product Name Screen Shot](.github/product.png)

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `twitter_handle`, `email_client`, `email`, `project_title`, `project_description`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Python][Python.org]][Python-url]
- [![Django][Django.com]][Django-url]
- [![Javascript][Javascript.com]][Javascript-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

Feel free to uitilize the already existing webpage for your needs. However, if you wish to self-host, follow the steps below.

### Prerequisites

We assume you are running on Ubuntu. As such, you will need to have the following set up:

- Python 3.6 or higher
- A Postgres database
- Apache, Nginx, or your favorite web server (we will assume you know how to set this up)
  - _SECURITY WARNING: In `settings.py`, we have set the allowed_hosts to `['_']`. This is not secure and should be changed to your domain name, or you need to have your web server checking for hostname.\*
- From a back-end standpoint, there are no logs. This is for privacy reasons and is deemed acceptable for this low-security project. However, you may want to set up logging for your own purposes.
- There are also no tests for this project. This is because the project's scope is simple and future changes are not forseen. However, you may want to set up tests for your own purposes.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/dscpsyl/loget-japan-tracker.git
   ```
2. Create a virtual environment and activate it
   ```sh
   python3 -m venv .venv && source .venv/bin/activate
   ```
3. Install the required packages
   ```sh
    pip install -r requirements.txt
   ```
4. Set up your environment variables in the Django project folder
   ```sh
   cd logettracker && touch .env
   ```
   You will need to set the following variables:
   ```sh
   DJANGO-SECRET-KEY
   ```
5. Setup your database connection. We want your Postgres to have a service named `logetcardtrackerdb_service` with the database name `loget_tracker`. In addition, create a `.my_pgpass` in the Django project folder to connect to your database. You can change how you want to connect to your database in the `settings.py` file.
6. Make the migrations
   ```sh
   python manage.py makemigrations && python manage.py migrate
   ```
7. Create a superuser
   ```sh
   python manage.py createsuperuser
   ```
8. Populate your cards table with the scraper.
   ```sh
   cd ../logetscraper && python main.py
   ```
9. If you are deploying to a production environment, make sure to run the deploy checks. Otherwise, enable DEBUG and remove other restrictions in the `settings.py` file for your own convenience.
   ```sh
   python manage.py check --deploy
   python manage.py collectstatic
   ```
10. Finally, start the server

```sh
cd ../logettracker && python manage.py runserver
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Usage is simple. Simply create an account on the website and login.

You will be redirected to the tracker page where you can select which cards you've already collected. Cards yet to be collected will be greyed out. You can also export your collection in the settings page. If at any time you wish to erase your existance from the site, you can delete your account in the settings page.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the AGPL-3.0 License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

<a href="https://github.com/dscpsyl/loget-japan-tracker/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=dscpsyl/loget-japan-tracker" />
</a>
<br/>
<br/>
  
[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/dscpsyl)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/dscpsyl/loget-japan-tracker.svg?style=for-the-badge
[contributors-url]: https://github.com/dscpsyl/loget-japan-tracker/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/dscpsyl/loget-japan-tracker.svg?style=for-the-badge
[forks-url]: https://github.com/dscpsyl/loget-japan-tracker/network/members
[stars-shield]: https://img.shields.io/github/stars/dscpsyl/loget-japan-tracker.svg?style=for-the-badge
[stars-url]: https://github.com/dscpsyl/loget-japan-tracker/stargazers
[issues-shield]: https://img.shields.io/github/issues/dscpsyl/loget-japan-tracker.svg?style=for-the-badge
[issues-url]: https://github.com/dscpsyl/loget-japan-tracker/issues
[license-shield]: https://img.shields.io/github/license/dscpsyl/loget-japan-tracker.svg?style=for-the-badge
[license-url]: https://github.com/dscpsyl/loget-japan-tracker/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/davidjsim
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Django.com]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[Javascript.com]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[Javascript-url]: https://www.javascript.com/
