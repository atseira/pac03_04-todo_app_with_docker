# Dua proyek jadi satu
Satu README.md ini akan menjelaskan project dari dua kelas Pacmann sekaligus, yaitu berkaitan tentang [Web Development](#webdev) dan [Linux & Container](#linux).

<h1 id="webdev">Web Development</h1>
(dalam pengerjaan)

<h1 id="linux">Linux & Container</h1>

## Latar Belakang
Men-deploy aplikasi web development dengan Docker dan contoh penggunaan bash script pada host Linux.

## Langkah-langkah penggunaan Docker
### Dockerfile
Rangkaian perintah untuk membangun image di file `Dockerfile`. File ini kita set supaya membaca file `requirements.txt`, yakni daftar library yang diperlukan untuk menjalankan aplikasi ini, menginstall-nya di command `RUN` dan lalu di-set agar dijalankan proses `flask` di `--host=0.0.0.0`.

### docker-compose.yml
Di file ini kita membuat 2 image sekaligus dan mengatur hubungan keduanya. Service `web` berkaitan dengan proses `flask` beserta pengaturan `environment`nya agar aplikasi bisa berjalan. Salah satu yang menjadi perhatian adalah bagaimana menghubungkan proses `flask` dengan database di image `postgres`. Diatur `URI` database-nya di `environment` dan dependensi-nya di `depends_on: - db`, yang mana `db` diatur di file .yml yang sama.

Aplikasi yang dijalankan `flask` dijalankan di port `5000` pada container dan dapat diakses di host, juga di port `5000`. Ini diatur lewat  `ports: - 5000:5000`

Di service `db` kita beri pengaturan database. Dengan pengaturan di .yml ini, database itu berjalan hanya di dalam container dan tidak di komputer host. Dalam konteks tahap development, PostgreSQL user, password, db terdata di dalam file .yml. Dalam tahap live, pengaturan ini perlu disesuaikan.

PostgreSQL ini dapat diakses di dalam container pada port 5432. Tapi jika kita ingin mengaksesnya dari host, dapat diakses di port 5433. Ini diatur lewat `ports: -5433:5342`.

Pengaturan `restart: always` adalah agar container PostgreSQL selalu di-restart jika terjadi kegagalan.

### Cara menjalankan aplikasi
Clone git ini ke komputer, lalu siapkan file .env berisi `SECRET_KEY`. Jalankan
```
py gen_secret_code.py
```
dan akan di-print `SECRET_KEY`. Salin key tersebut ke dalam file .env_example, simpan, dan ganti nama .env_example menjadi .env.

Install docker di komputer. Lalu di folder project ini, jalankan:
```
docker build -t todoapp .

docker-compose up
```
Line `docker-compose up` perlu diganti menjadi
```
docker-compose up --build
```
jika ada perubahan pada `Dockerfile` atau `docker-compose.yml`.