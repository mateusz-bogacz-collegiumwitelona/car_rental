--
-- PostgreSQL database cluster dump
--

-- Started on 2025-04-05 21:12:11

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE "user";
ALTER ROLE "user" WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:pUposaqObSx3cpRKhY7kDg==$5tYvdqdtRRvZF/QrZW7Q4ibEfYH+pYTu5THEWSDGcX4=:nuyYaiPOU4e7zowSdz1bcMo11D/BQeQ8ZtpDKbyphKE=';

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.2

-- Started on 2025-04-05 21:12:11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2025-04-05 21:12:11

--
-- PostgreSQL database dump complete
--

--
-- Database "dockerdjango" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.2

-- Started on 2025-04-05 21:12:11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3355 (class 1262 OID 16384)
-- Name: dockerdjango; Type: DATABASE; Schema: -; Owner: user
--

CREATE DATABASE dockerdjango WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE dockerdjango OWNER TO "user";

\connect dockerdjango

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2025-04-05 21:12:11

--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.2

-- Started on 2025-04-05 21:12:11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2025-04-05 21:12:11

--
-- PostgreSQL database dump complete
--

-- Completed on 2025-04-05 21:12:11

--
-- PostgreSQL database cluster dump complete
--

