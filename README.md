<!-- ![Logo]() -->

<h1 align="center">Skripsi</h1>

## Table of Contents

1. [Tech Stack](#tech-stack)
2. [Description](#description)
3. [Environment Variables](#environment-variables)
4. [Authors](#authors)

## Tech Stack

## **Client:**

-   React JS

## **Server:**

-   Python
-   Flask

## **ML Pipeline:**

-   Preprocessing
    -   DRMF
    -   DLIB
-   Feature
    -   POC
    -   4QMV
-   Classification
    -   KNN
    -   SVM

## Description

Project ini adalah.

-   Buat skripsi dan ...

---

## Used For ?

Project ini ditujukan.

-   Buat skripsi dan ...

---

## Environment Variables

Untuk menjalankan apps ini harus menyertakan .env yang bisa didapat dari .env.example

-   ### Backend
    -   `JWT_SECRET`
-   ### Frontend
    -   `JWT_KEY`

---

## Folder Structure

    .                           # root project
    ├── api-docs                # api documentation
    ├── db
    │   ├── db.sql              # database project
    │   └── ...
    ├── config-server
    │   ├── nginx.conf          # nginx configuration
    │   └── ...
    ├── dump
    ├── services
    │   ├── frontend            # frontend project
    │   ├── backend             # backend project
    |   └── ml-pipeline         # machine learning base
    |   └── ...
    └── ...

## Installation

Clone the project

```bash
  git clone ...
```

Go to the project directory

```bash
  cd ...
```

---

## Run Locally

Install dependencies

```bash
  make init
  make install
```

Start frontend

```bash
  make run-frontend
```

Start backend

```bash
  make run-backend
```

Start frontend and backend

```bash
  make start
```

Start build

```bash
  make build
```

Start testing

```bash
  make test
```

## Authors

-   [@BengakDev](https://github.com/DaNgak)

Made with ❤️ by BengakDev
