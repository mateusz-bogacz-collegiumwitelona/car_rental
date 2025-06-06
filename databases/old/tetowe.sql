PGDMP  /    0                }        
   car_rental    17.4 (Debian 17.4-1.pgdg120+2)    17.2 q    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16384 
   car_rental    DATABASE     u   CREATE DATABASE car_rental WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE car_rental;
                     admin    false            �            1255    16385    audyt_miasta()    FUNCTION     	  CREATE FUNCTION public.audyt_miasta() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    uzytkownik_record RECORD;
BEGIN
    IF (TG_OP = 'DELETE') THEN
        -- Dla każdego użytkownika powiązanego z tym miastem, zapisz kompletny rekord historii
        FOR uzytkownik_record IN (SELECT * FROM uzytkownicy WHERE id_zamieszkania = OLD.id_zamieszkania) LOOP
            INSERT INTO historia_zmian (
                tabela_zrodlowa, id_rekordu, operacja, 
                miasto, ulica, nr_ulicy, kod_pocztowy,
                id_user, imie, nazwisko, pesel, email, id_zamieszkania
            ) VALUES (
                'miasta', OLD.id_zamieszkania, 'DELETE',
                OLD.miasto, OLD.ulica, OLD.nr_ulicy, OLD.kod_pocztowy,
                uzytkownik_record.id_user, uzytkownik_record.imie, uzytkownik_record.nazwisko, 
                uzytkownik_record."PESEL", uzytkownik_record.email, uzytkownik_record.id_zamieszkania
            );
        END LOOP;
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        -- Dla każdego użytkownika powiązanego z tym miastem, zapisz kompletny rekord historii
        FOR uzytkownik_record IN (SELECT * FROM uzytkownicy WHERE id_zamieszkania = NEW.id_zamieszkania) LOOP
            INSERT INTO historia_zmian (
                tabela_zrodlowa, id_rekordu, operacja, 
                miasto, ulica, nr_ulicy, kod_pocztowy,
                id_user, imie, nazwisko, pesel, email, id_zamieszkania
            ) VALUES (
                'miasta', NEW.id_zamieszkania, 'UPDATE',
                NEW.miasto, NEW.ulica, NEW.nr_ulicy, NEW.kod_pocztowy,
                uzytkownik_record.id_user, uzytkownik_record.imie, uzytkownik_record.nazwisko, 
                uzytkownik_record."PESEL", uzytkownik_record.email, uzytkownik_record.id_zamieszkania
            );
        END LOOP;
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        -- Dla nowo dodanego miasta, możemy nie mieć jeszcze powiązanych użytkowników
        INSERT INTO historia_zmian (
            tabela_zrodlowa, id_rekordu, operacja, 
            miasto, ulica, nr_ulicy, kod_pocztowy
        ) VALUES (
            'miasta', NEW.id_zamieszkania, 'INSERT',
            NEW.miasto, NEW.ulica, NEW.nr_ulicy, NEW.kod_pocztowy
        );
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$;
 %   DROP FUNCTION public.audyt_miasta();
       public               admin    false            �            1255    16386    audyt_uzytkownicy()    FUNCTION     �  CREATE FUNCTION public.audyt_uzytkownicy() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    miasto_record RECORD;
BEGIN
    IF (TG_OP = 'DELETE') THEN
        -- Pobierz dane miasta i zapisz kompletny rekord
        SELECT * INTO miasto_record FROM miasta WHERE id_zamieszkania = OLD.id_zamieszkania;
        
        INSERT INTO historia_zmian (
            tabela_zrodlowa, id_rekordu, operacja,
            miasto, ulica, nr_ulicy, kod_pocztowy,
            id_user, imie, nazwisko, pesel, email, id_zamieszkania
        ) VALUES (
            'uzytkownicy', OLD.id_user, 'DELETE',
            miasto_record.miasto, miasto_record.ulica, miasto_record.nr_ulicy, miasto_record.kod_pocztowy,
            OLD.id_user, OLD.imie, OLD.nazwisko, OLD."PESEL", OLD.email, OLD.id_zamieszkania
        );
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        -- Pobierz dane miasta i zapisz kompletny rekord
        SELECT * INTO miasto_record FROM miasta WHERE id_zamieszkania = NEW.id_zamieszkania;
        
        INSERT INTO historia_zmian (
            tabela_zrodlowa, id_rekordu, operacja,
            miasto, ulica, nr_ulicy, kod_pocztowy,
            id_user, imie, nazwisko, pesel, email, id_zamieszkania
        ) VALUES (
            'uzytkownicy', NEW.id_user, 'UPDATE',
            miasto_record.miasto, miasto_record.ulica, miasto_record.nr_ulicy, miasto_record.kod_pocztowy,
            NEW.id_user, NEW.imie, NEW.nazwisko, NEW."PESEL", NEW.email, NEW.id_zamieszkania
        );
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        -- Pobierz dane miasta i zapisz kompletny rekord
        SELECT * INTO miasto_record FROM miasta WHERE id_zamieszkania = NEW.id_zamieszkania;
        
        INSERT INTO historia_zmian (
            tabela_zrodlowa, id_rekordu, operacja,
            miasto, ulica, nr_ulicy, kod_pocztowy,
            id_user, imie, nazwisko, pesel, email, id_zamieszkania
        ) VALUES (
            'uzytkownicy', NEW.id_user, 'INSERT',
            miasto_record.miasto, miasto_record.ulica, miasto_record.nr_ulicy, miasto_record.kod_pocztowy,
            NEW.id_user, NEW.imie, NEW.nazwisko, NEW."PESEL", NEW.email, NEW.id_zamieszkania
        );
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$;
 *   DROP FUNCTION public.audyt_uzytkownicy();
       public               admin    false            �            1259    16387    admin    TABLE     h  CREATE TABLE public.admin (
    id_admin integer NOT NULL,
    imie character varying(50) DEFAULT 'anonymous'::character varying NOT NULL,
    nazwisko character varying(50) DEFAULT 'unknown'::character varying NOT NULL,
    email character varying(50) DEFAULT 'example@example.com'::character varying NOT NULL,
    password character varying(255) NOT NULL
);
    DROP TABLE public.admin;
       public         heap r       admin    false            �            1259    16393    admin_id_admin_seq    SEQUENCE     �   CREATE SEQUENCE public.admin_id_admin_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.admin_id_admin_seq;
       public               admin    false    217            �           0    0    admin_id_admin_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.admin_id_admin_seq OWNED BY public.admin.id_admin;
          public               admin    false    218            �            1259    16394    auta    TABLE     ?  CREATE TABLE public.auta (
    id_auta integer NOT NULL,
    marka character varying(100) DEFAULT 'unknown'::character varying NOT NULL,
    model character varying(100) DEFAULT 'unknown'::character varying NOT NULL,
    rocznik integer NOT NULL,
    opis character varying(1000),
    osiagi character varying(1000)
);
    DROP TABLE public.auta;
       public         heap r       admin    false            �            1259    16401    auta_id_auta_seq    SEQUENCE     �   CREATE SEQUENCE public.auta_id_auta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.auta_id_auta_seq;
       public               admin    false    219            �           0    0    auta_id_auta_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.auta_id_auta_seq OWNED BY public.auta.id_auta;
          public               admin    false    220            �            1259    16402    auta_zdj    TABLE     �   CREATE TABLE public.auta_zdj (
    id_zdj integer NOT NULL,
    id_auta integer NOT NULL,
    zdj character varying(255) NOT NULL,
    kolejnosc integer DEFAULT 1,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.auta_zdj;
       public         heap r       admin    false            �            1259    16407    auta_zdj_id_zdj_seq    SEQUENCE     �   CREATE SEQUENCE public.auta_zdj_id_zdj_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.auta_zdj_id_zdj_seq;
       public               admin    false    221            �           0    0    auta_zdj_id_zdj_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.auta_zdj_id_zdj_seq OWNED BY public.auta_zdj.id_zdj;
          public               admin    false    222            �            1259    16408 
   auth_group    TABLE     f   CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
    DROP TABLE public.auth_group;
       public         heap r       admin    false            �            1259    16411    auth_group_id_seq    SEQUENCE     �   ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               admin    false    223            �            1259    16412    auth_group_permissions    TABLE     �   CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
 *   DROP TABLE public.auth_group_permissions;
       public         heap r       admin    false            �            1259    16415    auth_group_permissions_id_seq    SEQUENCE     �   ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               admin    false    225            �            1259    16416    auth_permission    TABLE     �   CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
 #   DROP TABLE public.auth_permission;
       public         heap r       admin    false            �            1259    16419    auth_permission_id_seq    SEQUENCE     �   ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               admin    false    227            �            1259    16420 	   auth_user    TABLE     �  CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
    DROP TABLE public.auth_user;
       public         heap r       admin    false            �            1259    16425    auth_user_groups    TABLE     ~   CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
 $   DROP TABLE public.auth_user_groups;
       public         heap r       admin    false            �            1259    16428    auth_user_groups_id_seq    SEQUENCE     �   ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               admin    false    230            �            1259    16429    auth_user_id_seq    SEQUENCE     �   ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               admin    false    229            �            1259    16430    auth_user_user_permissions    TABLE     �   CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
 .   DROP TABLE public.auth_user_user_permissions;
       public         heap r       admin    false            �            1259    16433 !   auth_user_user_permissions_id_seq    SEQUENCE     �   ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               admin    false    233            �            1259    16434    czarna_lista    TABLE       CREATE TABLE public.czarna_lista (
    id_bl integer NOT NULL,
    id_user integer NOT NULL,
    powod character varying(50) DEFAULT 'unknown'::character varying NOT NULL,
    data_poczatkowa date NOT NULL,
    data_koncowa date NOT NULL,
    id_admin integer NOT NULL
);
     DROP TABLE public.czarna_lista;
       public         heap r       admin    false            �            1259    16438    czarna_lista_id_bl_seq    SEQUENCE     �   CREATE SEQUENCE public.czarna_lista_id_bl_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.czarna_lista_id_bl_seq;
       public               admin    false    235            �           0    0    czarna_lista_id_bl_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.czarna_lista_id_bl_seq OWNED BY public.czarna_lista.id_bl;
          public               admin    false    236            �            1259    16439    django_admin_log    TABLE     �  CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
 $   DROP TABLE public.django_admin_log;
       public         heap r       admin    false            �            1259    16445    django_admin_log_id_seq    SEQUENCE     �   ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               admin    false    237            �            1259    16446    django_content_type    TABLE     �   CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
 '   DROP TABLE public.django_content_type;
       public         heap r       admin    false            �            1259    16449    django_content_type_id_seq    SEQUENCE     �   ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               admin    false    239            �            1259    16450    django_migrations    TABLE     �   CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
 %   DROP TABLE public.django_migrations;
       public         heap r       admin    false            �            1259    16455    django_migrations_id_seq    SEQUENCE     �   ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               admin    false    241            �            1259    16456    django_session    TABLE     �   CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
 "   DROP TABLE public.django_session;
       public         heap r       admin    false            �            1259    16461    historia_zmian    TABLE     U  CREATE TABLE public.historia_zmian (
    id_historii integer NOT NULL,
    tabela_zrodlowa character varying(50) NOT NULL,
    id_rekordu integer NOT NULL,
    operacja character varying(10) NOT NULL,
    data_operacji timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    miasto character varying(100),
    ulica character varying(100),
    nr_ulicy character varying(5),
    kod_pocztowy character varying(6),
    id_user integer,
    imie character varying(100),
    nazwisko character varying(100),
    pesel character(11),
    email character varying(50),
    id_zamieszkania integer
);
 "   DROP TABLE public.historia_zmian;
       public         heap r       admin    false            �            1259    16467    historia_zmian_id_historii_seq    SEQUENCE     �   CREATE SEQUENCE public.historia_zmian_id_historii_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.historia_zmian_id_historii_seq;
       public               admin    false    244            �           0    0    historia_zmian_id_historii_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.historia_zmian_id_historii_seq OWNED BY public.historia_zmian.id_historii;
          public               admin    false    245            �            1259    16468    miasta    TABLE     �  CREATE TABLE public.miasta (
    id_zamieszkania integer NOT NULL,
    miasto character varying(100) DEFAULT 'city_name'::character varying NOT NULL,
    ulica character varying(100) DEFAULT 'ulica'::character varying NOT NULL,
    nr_ulicy character varying(5) DEFAULT '1b'::character varying NOT NULL,
    kod_pocztowy character varying(6) DEFAULT '12-345'::character varying NOT NULL
);
    DROP TABLE public.miasta;
       public         heap r       admin    false            �            1259    16475    miasta_id_zamieszkania_seq    SEQUENCE     �   CREATE SEQUENCE public.miasta_id_zamieszkania_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.miasta_id_zamieszkania_seq;
       public               admin    false    246            �           0    0    miasta_id_zamieszkania_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.miasta_id_zamieszkania_seq OWNED BY public.miasta.id_zamieszkania;
          public               admin    false    247            �            1259    16476    uzytkownicy    TABLE     �  CREATE TABLE public.uzytkownicy (
    id_user integer NOT NULL,
    imie character varying(100) DEFAULT 'unknown'::character varying NOT NULL,
    nazwisko character varying(100) DEFAULT 'unknown'::character varying NOT NULL,
    "PESEL" character(11) DEFAULT '00000000000'::bpchar NOT NULL,
    email character varying(50) DEFAULT 'example@example.com'::character varying NOT NULL,
    haslo character varying(100) NOT NULL,
    id_zamieszkania integer NOT NULL
);
    DROP TABLE public.uzytkownicy;
       public         heap r       admin    false            �            1259    16483    uzytkownicy_id_user_seq    SEQUENCE     �   CREATE SEQUENCE public.uzytkownicy_id_user_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.uzytkownicy_id_user_seq;
       public               admin    false    248            �           0    0    uzytkownicy_id_user_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.uzytkownicy_id_user_seq OWNED BY public.uzytkownicy.id_user;
          public               admin    false    249            �            1259    16484    wypozyczenie    TABLE     �   CREATE TABLE public.wypozyczenie (
    id_wypozyczenia integer NOT NULL,
    data_poczatkowa date NOT NULL,
    data_koncowa date NOT NULL,
    id_auta integer NOT NULL,
    id_user integer NOT NULL
);
     DROP TABLE public.wypozyczenie;
       public         heap r       admin    false            �            1259    16487     wypozyczenie_id_wypozyczenia_seq    SEQUENCE     �   CREATE SEQUENCE public.wypozyczenie_id_wypozyczenia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.wypozyczenie_id_wypozyczenia_seq;
       public               admin    false    250            �           0    0     wypozyczenie_id_wypozyczenia_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.wypozyczenie_id_wypozyczenia_seq OWNED BY public.wypozyczenie.id_wypozyczenia;
          public               admin    false    251            �           2604    16488    admin id_admin    DEFAULT     p   ALTER TABLE ONLY public.admin ALTER COLUMN id_admin SET DEFAULT nextval('public.admin_id_admin_seq'::regclass);
 =   ALTER TABLE public.admin ALTER COLUMN id_admin DROP DEFAULT;
       public               admin    false    218    217            �           2604    16489    auta id_auta    DEFAULT     l   ALTER TABLE ONLY public.auta ALTER COLUMN id_auta SET DEFAULT nextval('public.auta_id_auta_seq'::regclass);
 ;   ALTER TABLE public.auta ALTER COLUMN id_auta DROP DEFAULT;
       public               admin    false    220    219            �           2604    16490    auta_zdj id_zdj    DEFAULT     r   ALTER TABLE ONLY public.auta_zdj ALTER COLUMN id_zdj SET DEFAULT nextval('public.auta_zdj_id_zdj_seq'::regclass);
 >   ALTER TABLE public.auta_zdj ALTER COLUMN id_zdj DROP DEFAULT;
       public               admin    false    222    221            �           2604    16491    czarna_lista id_bl    DEFAULT     x   ALTER TABLE ONLY public.czarna_lista ALTER COLUMN id_bl SET DEFAULT nextval('public.czarna_lista_id_bl_seq'::regclass);
 A   ALTER TABLE public.czarna_lista ALTER COLUMN id_bl DROP DEFAULT;
       public               admin    false    236    235            �           2604    16492    historia_zmian id_historii    DEFAULT     �   ALTER TABLE ONLY public.historia_zmian ALTER COLUMN id_historii SET DEFAULT nextval('public.historia_zmian_id_historii_seq'::regclass);
 I   ALTER TABLE public.historia_zmian ALTER COLUMN id_historii DROP DEFAULT;
       public               admin    false    245    244            �           2604    16493    miasta id_zamieszkania    DEFAULT     �   ALTER TABLE ONLY public.miasta ALTER COLUMN id_zamieszkania SET DEFAULT nextval('public.miasta_id_zamieszkania_seq'::regclass);
 E   ALTER TABLE public.miasta ALTER COLUMN id_zamieszkania DROP DEFAULT;
       public               admin    false    247    246            �           2604    16494    uzytkownicy id_user    DEFAULT     z   ALTER TABLE ONLY public.uzytkownicy ALTER COLUMN id_user SET DEFAULT nextval('public.uzytkownicy_id_user_seq'::regclass);
 B   ALTER TABLE public.uzytkownicy ALTER COLUMN id_user DROP DEFAULT;
       public               admin    false    249    248            �           2604    16495    wypozyczenie id_wypozyczenia    DEFAULT     �   ALTER TABLE ONLY public.wypozyczenie ALTER COLUMN id_wypozyczenia SET DEFAULT nextval('public.wypozyczenie_id_wypozyczenia_seq'::regclass);
 K   ALTER TABLE public.wypozyczenie ALTER COLUMN id_wypozyczenia DROP DEFAULT;
       public               admin    false    251    250            �           2606    16497    admin admin_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (id_admin);
 :   ALTER TABLE ONLY public.admin DROP CONSTRAINT admin_pkey;
       public                 admin    false    217            �           2606    16499    auta auta_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.auta
    ADD CONSTRAINT auta_pkey PRIMARY KEY (id_auta);
 8   ALTER TABLE ONLY public.auta DROP CONSTRAINT auta_pkey;
       public                 admin    false    219            �           2606    16501    auta_zdj auta_zdj_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.auta_zdj
    ADD CONSTRAINT auta_zdj_pkey PRIMARY KEY (id_zdj);
 @   ALTER TABLE ONLY public.auta_zdj DROP CONSTRAINT auta_zdj_pkey;
       public                 admin    false    221                       2606    16503    auth_group auth_group_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
       public                 admin    false    223                       2606    16505 R   auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
 |   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
       public                 admin    false    225    225                       2606    16507 2   auth_group_permissions auth_group_permissions_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
       public                 admin    false    225                       2606    16509    auth_group auth_group_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
       public                 admin    false    223                       2606    16511 F   auth_permission auth_permission_content_type_id_codename_01ab375a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
 p   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
       public                 admin    false    227    227                       2606    16513 $   auth_permission auth_permission_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
       public                 admin    false    227                       2606    16515 &   auth_user_groups auth_user_groups_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
       public                 admin    false    230                       2606    16517 @   auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);
 j   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq;
       public                 admin    false    230    230                       2606    16519    auth_user auth_user_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
       public                 admin    false    229                       2606    16521 :   auth_user_user_permissions auth_user_user_permissions_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
       public                 admin    false    233            !           2606    16523 Y   auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
       public                 admin    false    233    233                       2606    16525     auth_user auth_user_username_key 
   CONSTRAINT     _   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);
 J   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
       public                 admin    false    229            #           2606    16527    czarna_lista czarna_lista_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.czarna_lista
    ADD CONSTRAINT czarna_lista_pkey PRIMARY KEY (id_bl);
 H   ALTER TABLE ONLY public.czarna_lista DROP CONSTRAINT czarna_lista_pkey;
       public                 admin    false    235            &           2606    16529 &   django_admin_log django_admin_log_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
       public                 admin    false    237            )           2606    16531 E   django_content_type django_content_type_app_label_model_76bd3d3b_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
 o   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
       public                 admin    false    239    239            +           2606    16533 ,   django_content_type django_content_type_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
       public                 admin    false    239            -           2606    16535 (   django_migrations django_migrations_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
       public                 admin    false    241            0           2606    16537 "   django_session django_session_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
 L   ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
       public                 admin    false    243            3           2606    16539 "   historia_zmian historia_zmian_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.historia_zmian
    ADD CONSTRAINT historia_zmian_pkey PRIMARY KEY (id_historii);
 L   ALTER TABLE ONLY public.historia_zmian DROP CONSTRAINT historia_zmian_pkey;
       public                 admin    false    244            5           2606    16541    miasta miasta_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.miasta
    ADD CONSTRAINT miasta_pkey PRIMARY KEY (id_zamieszkania);
 <   ALTER TABLE ONLY public.miasta DROP CONSTRAINT miasta_pkey;
       public                 admin    false    246            7           2606    16543    uzytkownicy uzytkownicy_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.uzytkownicy
    ADD CONSTRAINT uzytkownicy_pkey PRIMARY KEY (id_user);
 F   ALTER TABLE ONLY public.uzytkownicy DROP CONSTRAINT uzytkownicy_pkey;
       public                 admin    false    248            9           2606    16545    wypozyczenie wypozyczenie_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.wypozyczenie
    ADD CONSTRAINT wypozyczenie_pkey PRIMARY KEY (id_wypozyczenia);
 H   ALTER TABLE ONLY public.wypozyczenie DROP CONSTRAINT wypozyczenie_pkey;
       public                 admin    false    250                       1259    16546    auth_group_name_a6ea08ec_like    INDEX     h   CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
 1   DROP INDEX public.auth_group_name_a6ea08ec_like;
       public                 admin    false    223                       1259    16547 (   auth_group_permissions_group_id_b120cbf9    INDEX     o   CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
 <   DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
       public                 admin    false    225            	           1259    16548 -   auth_group_permissions_permission_id_84c5c92e    INDEX     y   CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
 A   DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
       public                 admin    false    225                       1259    16549 (   auth_permission_content_type_id_2f476e4b    INDEX     o   CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
 <   DROP INDEX public.auth_permission_content_type_id_2f476e4b;
       public                 admin    false    227                       1259    16550 "   auth_user_groups_group_id_97559544    INDEX     c   CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);
 6   DROP INDEX public.auth_user_groups_group_id_97559544;
       public                 admin    false    230                       1259    16551 !   auth_user_groups_user_id_6a12ed8b    INDEX     a   CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);
 5   DROP INDEX public.auth_user_groups_user_id_6a12ed8b;
       public                 admin    false    230                       1259    16552 1   auth_user_user_permissions_permission_id_1fbb5f2c    INDEX     �   CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);
 E   DROP INDEX public.auth_user_user_permissions_permission_id_1fbb5f2c;
       public                 admin    false    233                       1259    16553 +   auth_user_user_permissions_user_id_a95ead1b    INDEX     u   CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);
 ?   DROP INDEX public.auth_user_user_permissions_user_id_a95ead1b;
       public                 admin    false    233                       1259    16554     auth_user_username_6821ab7c_like    INDEX     n   CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);
 4   DROP INDEX public.auth_user_username_6821ab7c_like;
       public                 admin    false    229            $           1259    16555 )   django_admin_log_content_type_id_c4bce8eb    INDEX     q   CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
 =   DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
       public                 admin    false    237            '           1259    16556 !   django_admin_log_user_id_c564eba6    INDEX     a   CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
 5   DROP INDEX public.django_admin_log_user_id_c564eba6;
       public                 admin    false    237            .           1259    16557 #   django_session_expire_date_a5c62663    INDEX     e   CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
 7   DROP INDEX public.django_session_expire_date_a5c62663;
       public                 admin    false    243            1           1259    16558 (   django_session_session_key_c0390e0f_like    INDEX     ~   CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
 <   DROP INDEX public.django_session_session_key_c0390e0f_like;
       public                 admin    false    243                        1259    16559    idx_auto_zdjecia_id_auta    INDEX     P   CREATE INDEX idx_auto_zdjecia_id_auta ON public.auta_zdj USING btree (id_auta);
 ,   DROP INDEX public.idx_auto_zdjecia_id_auta;
       public                 admin    false    221            I           2620    16560    miasta trigger_miasta_audyt    TRIGGER     �   CREATE TRIGGER trigger_miasta_audyt AFTER INSERT OR DELETE OR UPDATE ON public.miasta FOR EACH ROW EXECUTE FUNCTION public.audyt_miasta();
 4   DROP TRIGGER trigger_miasta_audyt ON public.miasta;
       public               admin    false    246    252            J           2620    16561 %   uzytkownicy trigger_uzytkownicy_audyt    TRIGGER     �   CREATE TRIGGER trigger_uzytkownicy_audyt AFTER INSERT OR DELETE OR UPDATE ON public.uzytkownicy FOR EACH ROW EXECUTE FUNCTION public.audyt_uzytkownicy();
 >   DROP TRIGGER trigger_uzytkownicy_audyt ON public.uzytkownicy;
       public               admin    false    248    253            :           2606    16562    auta_zdj auta_zdj_id_auta_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.auta_zdj
    ADD CONSTRAINT auta_zdj_id_auta_fkey FOREIGN KEY (id_auta) REFERENCES public.auta(id_auta) ON DELETE CASCADE;
 H   ALTER TABLE ONLY public.auta_zdj DROP CONSTRAINT auta_zdj_id_auta_fkey;
       public               admin    false    219    3325    221            ;           2606    16567 O   auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
       public               admin    false    225    3344    227            <           2606    16572 P   auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
       public               admin    false    225    3333    223            =           2606    16577 E   auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 o   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
       public               admin    false    3371    227    239            >           2606    16582 D   auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 n   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id;
       public               admin    false    230    223    3333            ?           2606    16587 B   auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
       public               admin    false    230    229    3346            @           2606    16592 S   auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 }   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
       public               admin    false    227    3344    233            A           2606    16597 V   auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
       public               admin    false    233    229    3346            D           2606    16602 G   django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 q   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
       public               admin    false    239    237    3371            E           2606    16607 B   django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
       public               admin    false    3346    237    229            B           2606    16612    czarna_lista fk_admin_blacklist    FK CONSTRAINT     �   ALTER TABLE ONLY public.czarna_lista
    ADD CONSTRAINT fk_admin_blacklist FOREIGN KEY (id_admin) REFERENCES public.admin(id_admin) ON DELETE SET NULL;
 I   ALTER TABLE ONLY public.czarna_lista DROP CONSTRAINT fk_admin_blacklist;
       public               admin    false    217    235    3323            G           2606    16617    wypozyczenie fk_auto    FK CONSTRAINT     �   ALTER TABLE ONLY public.wypozyczenie
    ADD CONSTRAINT fk_auto FOREIGN KEY (id_auta) REFERENCES public.auta(id_auta) ON DELETE CASCADE;
 >   ALTER TABLE ONLY public.wypozyczenie DROP CONSTRAINT fk_auto;
       public               admin    false    3325    250    219            F           2606    16622    uzytkownicy fk_miasta    FK CONSTRAINT     �   ALTER TABLE ONLY public.uzytkownicy
    ADD CONSTRAINT fk_miasta FOREIGN KEY (id_zamieszkania) REFERENCES public.miasta(id_zamieszkania) ON DELETE CASCADE;
 ?   ALTER TABLE ONLY public.uzytkownicy DROP CONSTRAINT fk_miasta;
       public               admin    false    3381    246    248            C           2606    16627    czarna_lista fk_user_blacklist    FK CONSTRAINT     �   ALTER TABLE ONLY public.czarna_lista
    ADD CONSTRAINT fk_user_blacklist FOREIGN KEY (id_user) REFERENCES public.uzytkownicy(id_user) ON DELETE CASCADE;
 H   ALTER TABLE ONLY public.czarna_lista DROP CONSTRAINT fk_user_blacklist;
       public               admin    false    3383    235    248            H           2606    16632    wypozyczenie fk_uzytkownik    FK CONSTRAINT     �   ALTER TABLE ONLY public.wypozyczenie
    ADD CONSTRAINT fk_uzytkownik FOREIGN KEY (id_user) REFERENCES public.uzytkownicy(id_user) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.wypozyczenie DROP CONSTRAINT fk_uzytkownik;
       public               admin    false    3383    248    250           