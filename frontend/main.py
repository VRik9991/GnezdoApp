import sys
from pathlib import Path
import os
import streamlit as st
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.data.clans import ALL_CLANS
from api.backend_api import APIClient
import streamlit_authenticator as stauth
import hashlib
import yaml
import random
import json

st.set_page_config(initial_sidebar_state="collapsed")


def _hide_sidebar() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )


_AUTH_CONFIG_PATH = Path(__file__).with_name("auth_config.yaml")
with _AUTH_CONFIG_PATH.open("r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

@st.cache_data(show_spinner=False)
def _load_discipline_translations() -> tuple[dict[str, str], dict[str, str]]:
    path = PROJECT_ROOT / "backend" / "data" / "disciplines.json"
    if not path.exists():
        return {}, {}
    data = json.loads(path.read_text(encoding="utf-8"))
    discipline_map: dict[str, str] = {}
    power_map: dict[str, str] = {}

    discipline_fallback_ru: dict[str, str] = {
        "Umbrakinesis": "Умбракинез",
        "Hematurgy": "Гематургия",
        "Aethercraft": "Эфирокрафт",
    }
    power_fallback_ru: dict[str, str] = {
        "Veil Step": "Шаг сквозь завесу",
        "Sanguine Lattice": "Кровавая решетка",
        "Crimson Tide": "Багровый прилив",
        "Starbind": "Звездные узы",
    }

    def _is_placeholder_ru(value: object) -> bool:
        if not isinstance(value, str):
            return True
        text = value.strip()
        if not text:
            return True
        return set(text) <= {"?", " "}

    for discipline in data.get("disciplines", []):
        if not isinstance(discipline, dict):
            continue
        name = discipline.get("name", {})
        en = name.get("en")
        ru = name.get("ru")
        if isinstance(en, str):
            en = en.strip()
            ru_value = ru.strip() if isinstance(ru, str) else ""
            if ru_value and not _is_placeholder_ru(ru_value):
                discipline_map[en] = ru_value
                discipline_map[en.casefold()] = ru_value
            elif en in discipline_fallback_ru:
                discipline_map[en] = discipline_fallback_ru[en]
                discipline_map[en.casefold()] = discipline_fallback_ru[en]

        sub_items = discipline.get("поддисциплины", []) or []
        if not sub_items:
            for value in discipline.values():
                if not isinstance(value, list):
                    continue
                if any(
                    isinstance(entry, dict)
                    and isinstance(entry.get("name"), dict)
                    and isinstance(entry["name"].get("en"), str)
                    for entry in value
                ):
                    sub_items = value
                    break

        for sub in sub_items:
            if not isinstance(sub, dict):
                continue
            sub_name = sub.get("name", {})
            sub_en = sub_name.get("en")
            sub_ru = sub_name.get("ru")
            if isinstance(sub_en, str):
                sub_en = sub_en.strip()
                sub_ru_value = sub_ru.strip() if isinstance(sub_ru, str) else ""
                if sub_ru_value and not _is_placeholder_ru(sub_ru_value):
                    power_map[sub_en] = sub_ru_value
                    power_map[sub_en.casefold()] = sub_ru_value
                elif sub_en in power_fallback_ru:
                    power_map[sub_en] = power_fallback_ru[sub_en]
                    power_map[sub_en.casefold()] = power_fallback_ru[sub_en]

    for en, ru in discipline_fallback_ru.items():
        discipline_map.setdefault(en, ru)
        discipline_map.setdefault(en.casefold(), ru)
    for en, ru in power_fallback_ru.items():
        power_map.setdefault(en, ru)
        power_map.setdefault(en.casefold(), ru)

    return discipline_map, power_map


def _maybe_hash_passwords_inplace(auth_config: dict) -> bool:
    usernames = (((auth_config or {}).get("credentials") or {}).get("usernames") or {})
    passwords = []
    user_keys = []
    for user_key, user_data in usernames.items():
        password = (user_data or {}).get("password")
        if not isinstance(password, str) or not password:
            continue
        if not stauth.Hasher.is_hash(password):
            passwords.append(password)
            user_keys.append(user_key)

    if not passwords:
        return False

    hashed = stauth.Hasher.hash_list(passwords)
    for user_key, hashed_password in zip(user_keys, hashed, strict=True):
        usernames[user_key]["password"] = hashed_password
    return True

api = APIClient("http://localhost:8000")
_hashed_any = _maybe_hash_passwords_inplace(config)

authenticator = stauth.Authenticate(
        api.user_credentials(),
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )


_login_title = st.empty()
_login_caption = st.empty()
_login_title.title("Вход")

authenticator.login(location="main", key="Login")
name = st.session_state.get("name")
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")

if authentication_status is True:
    _login_title.empty()
    _login_caption.empty()

if authentication_status is not True:
    _hide_sidebar()
    _login_caption.caption("Введите логин и пароль, чтобы открыть приложение.")
    if authentication_status is False:
        st.error("Неверный логин или пароль.")
    st.stop()

# ---- Создаём аутентификатор ----
def Profile():
    
    
    if authentication_status:
        user = api.get_user(st.session_state.get("username"))
        

        user_stats = user.get("stats") or {}
        raw_disciplines = user_stats.get("disciplines") or []
        discipline_name_ru, power_name_ru = _load_discipline_translations()

        user_clan = user_stats.get("clan")
        clan_display = "Неизвестный клан"

        def _normalize_clan(value: object) -> str:
            return str(value or "").strip().casefold().replace("_", " ").replace("-", " ")

        user_clan_norm = _normalize_clan(user_clan)
        for clan in ALL_CLANS:
            if user_clan_norm and user_clan_norm in {
                _normalize_clan(clan.key),
                _normalize_clan(clan.name),
                _normalize_clan(clan.name_ru),
            }:
                clan_display = clan.name_ru or clan.name
                break

        disciplines_map = {}
        for item in raw_disciplines:
            discipline_en = str(item.get("discipline_en") or "").strip()
            power_en = str(item.get("power_en") or "").strip()

            discipline_name = (
                discipline_name_ru.get(discipline_en)
                or discipline_name_ru.get(discipline_en.casefold())
                or discipline_en
                or "Unknown discipline"
            )
            power_name = (
                power_name_ru.get(power_en)
                or power_name_ru.get(power_en.casefold())
                or power_en
                or "Unknown power"
            )
            disciplines_map.setdefault(discipline_name, []).append(
                {
                    "name": power_name,
                    "level": item.get("level") or 0,
                    "description": item.get("description") or "",
                }
            )

        character = {
            "photo": user["foto"],
            "name": user["character_name"],
            "alt_names": user["other_character_name"],
            "player_name": f"{user['name']} {user['last_name'][:1]}.",
            "shreknet": user["tg_name"],
            "status": "Активен",        # или "Торпор"
            "is_torpor": False,          # включи True — появится кнопка выхода
            "disciplines": disciplines_map,
            "morality": {
                "humanity": 7,
                "feeding": "Согласованное",
                "beast_image": "Голодный волк",
                "principles": [
                    {"name": "Не убивать невинных", "pillar": "Сострадание"},
                    {"name": "Держать слово", "pillar": "Честь"},
                ],
            },
            "resources": {
                "heart_dew": 12,
                "materials": 340,
                "territories": [
                    {"name": "Старый порт", "status": "Под контролем"},
                    {"name": "Северный рынок", "status": "Оспаривается"},
                ],
            },
        }


        st.divider()

        col1, col2 = st.columns([1, 2], gap="large")

        # ---- Фото ----
        with col1:
            st.image(character["photo"], width=230)

        # ---- Инфо ----
        with col2:
            st.subheader(character["name"])

            st.markdown(f"**Другие имена:** {character['alt_names']}")
            st.markdown(f"**Имя игрока:** {character['player_name']}")
            st.markdown(f"**Ник в Шрекнете:** {character['shreknet']}")

            # Статус
            if character["is_torpor"]:
                st.error("⚰️ ПЕРСОНАЖ В ТОРПОРЕ")
            else:
                st.success(f"Статус: {character['status']}")

            # Кнопки
            st.button("Сделать заявку", use_container_width=True)
            st.button("Загрузка?", use_container_width=True)

            # Только если персонаж в торпоре
            if character["is_torpor"]:
                st.button("Выйти из торпора", type="primary", use_container_width=True)

        # =========================================================
        st.divider()
        # =========================================================

        
        if "hunger_value" not in st.session_state:
            st.session_state.hunger_value = user['stats']["hunger"]

        @st.dialog("Клан")
        def modal_clan():
            st.write(user['stats']["clan_hint"])

        @st.dialog("Сир")
        def modal_sir_namee():
            st.write(user['stats']["sir_name_hint"])

        @st.dialog("Здоровье")
        def modal_health():
            st.write(user['stats']["health_hint"])

        @st.dialog("Диаблери")
        def modal_diablerie():
            st.write(user['stats']["diablerie_hint"])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Клан")
            st.write(f"**{clan_display}**")
            st.button("Подсказка", key="clan_hint_btn", on_click=modal_clan)

        with col2:
            st.subheader("Сир")
            st.write(f"**{user['stats']['sir_name']}**")
            st.button("Подсказка", key="sir_name_hint_btn", on_click=modal_sir_namee)

        with col3:
            st.subheader("Поколение")
            gen = user['stats']["generation"] + user['stats']["generation_mod"]
            st.metric("Генерация", gen)
            st.caption(f"База: {user['stats']['generation']}  |  Модификатор: {user['stats']['generation_mod']}")

        st.markdown("---")

        # ---------------------------- Здоровье / Голод ----------------------------

        st.subheader("Основные ресурсы")

        colA, colB = st.columns(2)

        with colA:
            st.metric("Здоровье", f"{user['stats']['health']} / 6")
            st.button("Что это?", key="health_hint_btn", on_click=modal_health)

        with colB:
            st.metric("Голод", f"{st.session_state.hunger_value} / 10")
            col_minus, col_plus = st.columns([1, 1])
            
            with col_minus:
                if st.button('minus', key="hunger_minus"):
                    st.session_state.hunger_value = max(0, st.session_state.hunger_value - 1)
                    user["stats"]["hunger"] = st.session_state.hunger_value
                    api.put_user(user)
                    st.rerun()
            with col_plus:
                if st.button('plus', key="hunger_plus"):
                    st.session_state.hunger_value = max(0, st.session_state.hunger_value + 1)
                    user["stats"]["hunger"] = st.session_state.hunger_value
                    api.put_user(user)
                    st.rerun()


        # ---------------------------- Сила / Стамина ----------------------------

        st.subheader("Физические параметры")

        colX, colY = st.columns(2)

        with colX:
            st.metric(
                "Сила",
                value=user['stats']["strength"] + user['stats']["strength_mod"],
                delta=f"+{user['stats']['strength_mod']} мод."
            )
            st.caption(f"База: {user['stats']['strength']}")

        with colY:
            st.metric(
                "Стамина",
                value=user['stats']["stamina"] + user['stats']["stamina_mod"],
                delta=f"+{user['stats']['stamina_mod']} мод."
            )
            st.caption(f"База: {user['stats']['stamina']}")

        # ---------------------------- Флаги ----------------------------

        st.subheader("Статусные флаги")

        colF1, colF2, colF3, colF4 = st.columns(4)

        with colF1:
            st.checkbox("Ритуалист", user['stats']["ritualist"], disabled=True)

        with colF2:
            st.checkbox("Уворот", user['stats']["dodge"], disabled=True)

        with colF3:
            st.checkbox("Истинная вера", user['stats']["true_faith"], disabled=True)

        with colF4:
            st.checkbox("Ощущается инферналистом", user['stats']["feels_infernalist"], disabled=True)

        # ---------------------------- Другие статусы ----------------------------

        st.subheader("Другие статусы")
        st.info(user['stats']["extra_status"])

        # ---------------------------- Кнопки ----------------------------

        st.markdown("### Системные действия")

        if user['stats']["torpor_button"]:
            st.button("⚰️ Впасть в торпор (фиксировано)", use_container_width=True)

        st.button("Меня диаблерят", use_container_width=True, on_click=modal_diablerie)

        # ДОПОЛНЕНИЕ: БЛОКИ 3-5 (Streamlit, совместимо с @st.dialog)
        # ВСТАВЛЯТЬ В КОНЕЦ ФАЙЛА ПОСЛЕ БЛОКА 2

        # =========================================================
        # БЛОК 3 — ДИСЦИПЛИНЫ
        # =========================================================

        st.divider()
        st.header("Дисциплины")

        @st.dialog("Способность")
        def ability_dialog(name, discipline, level, description):
            st.markdown(
                f"""
**Имя:** {name}  
**Дисциплина:** {discipline}  
**Уровень:** {level}
"""
            )
            if description:
                st.markdown(description)

        st.button(
            "➕ Заявка на изучение дисциплины",
            use_container_width=True
        )

        for discipline, abilities in character["disciplines"].items():
            with st.expander(discipline, expanded=True):
                for i, ab in enumerate(abilities):
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.write(f"**{ab['name']}** (Ур. {ab['level']})")
                    with c2:
                        st.button(
                            "ℹ️",
                            key=f"ab_{discipline}_{i}",
                            on_click=ability_dialog,
                            args=(ab["name"], discipline, ab["level"], ab["description"])
                        )

        # =========================================================
        # БЛОК 4 — МОРАЛЬ
        # =========================================================

        st.divider()
        st.header("Мораль")

        @st.dialog("Человечность")
        def humanity_dialog():
            st.write("Отражает степень утраты человеческой природы.")

        @st.dialog("Тип питания")
        def feeding_dialog():
            st.write("Определяет допустимые способы утоления голода.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Человечность", character["morality"]["humanity"])
            st.button("ℹ️", key="humanity_info", on_click=humanity_dialog)

        with col2:
            st.write(f"**Тип питания:** {character['morality']['feeding']}")
            st.button("ℹ️", key="feeding_info", on_click=feeding_dialog)

        with col3:
            st.write(f"**Образ зверя:** {character['morality']['beast_image']}")

        st.subheader("Принципы")

        if "principle_timers" not in st.session_state:
            st.session_state.principle_timers = {}

        for i, p in enumerate(character["morality"]["principles"]):
            c1, c2, c3 = st.columns([4, 1, 1])
            with c1:
                st.write(f"• **{p['name']}** — опора: *{p['pillar']}*")
            with c2:
                if st.button("⬇️ Принцип", key=f"drop_principle_{i}"):
                    st.session_state.principle_timers[i] = "principle"
                    st.warning("Принцип уронен. Запущен таймер.")
            with c3:
                if st.button("⬇️ Опора", key=f"drop_pillar_{i}"):
                    st.session_state.principle_timers[i] = "pillar"
                    st.warning("Опора уронена. Запущен таймер.")

        st.button("➕ Добавить принцип", help="Предзаполненная заявка")

        # =========================================================
        # БЛОК 5 — НАКОПЛЕНИЯ
        # =========================================================

        st.divider()
        st.header("Накопления")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Сердечная роса", character["resources"]["heart_dew"])

        with c2:
            st.metric("Ресурсы", character["resources"]["materials"])

        @st.dialog("Территория")
        def territory_dialog(name, status):
            st.markdown(f"""
        **Территория:** {name}  
        **Статус:** {status}
        """)

        st.subheader("Территории")

        for i, t in enumerate(character["resources"]["territories"]):
            st.button(
                f"{t['name']} — {t['status']}",
                key=f"territory_{i}",
                use_container_width=True,
                on_click=territory_dialog,
                args=(t["name"], t["status"])
            )


    news_db = [
        {
            "id": 1,
            "author": "Игрок1",
            "avatar": "https://i.pravatar.cc/50?img=1",
            "title": "Первая новость",
            "content": "Полный текст новости номер один...",
            "status": "Актуален",
            "likes": [],
            "dislikes": [],
            "comments": [
                {"nick": "Игрок2", "avatar": "https://i.pravatar.cc/50?img=2", "text": "Отличная новость!"}
            ],
            "created": 1,
            "history": [{"who": "Игрок1", "when": 1, "action": "Создано"}]
        },
        {
            "id": 2,
            "author": "Мастер1",
            "avatar": "https://i.pravatar.cc/50?img=3",
            "title": "Новость от мастера",
            "content": "Полный текст новости от мастера...",
            "status": "Актуален",
            "likes": [],
            "dislikes": [],
            "comments": [],
            "created": 1,
            "history": [{"who": "Мастер1", "when": 1, "action": "Создано"}]
        }
    ]

    def filter_news(news_list, hide_non_masters=False, hide_nicks=[]):
        filtered = []
        for news in news_list:
            if news['status'] != "Актуален":
                continue
            if hide_non_masters and "Мастер" not in news['author']:
                continue
            if news['author'] in hide_nicks:
                continue
            filtered.append(news)
        return sorted(filtered, key=lambda x: x['created'], reverse=True)

# #def News():
#     st.sidebar.title("Фильтры новостей")
#     hide_non_masters = st.sidebar.checkbox("Скрыть новости не от мастеров")
#     hide_nicks = st.sidebar.text_input("Скрыть новости от ников (через запятую)").split(",")
#     hide_nicks = [nick.strip() for nick in hide_nicks if nick.strip()]

#     news_to_show = filter_news(news_db, hide_non_masters, hide_nicks)

#     for news in news_to_show:
#         st.markdown("---")
#         cols = st.columns([1, 5])
#         with cols[0]:
#             st.image(news['avatar'], width=50)
#         with cols[1]:
#             st.subheader(f"{news['author']} — {news['title']}")
#             st.write(news['content'][:100] + "...")  # Обрезанное содержание
#             if st.button(f"Читать полностью (id={news['id']})"):
#                 show_full_news(news)

# #def show_full_news(news):
#     st.markdown("---")
#     cols = st.columns([1, 5])
#     with cols[0]:
#         st.image(news['avatar'], width=70)
#     with cols[1]:
#         st.subheader(news['author'])

#     # IT-комментарий (для мастеров)
#     st.text_area("IT-комментарий (ИТ:)", "")

#     # Полное содержание
#     st.write(news['content'])

#     # Место для картинки (пока просто выводим аватар)
#     st.image(news['avatar'], width=200)

#     # Лайки и дизлайки
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button(f"👍 Лайк ({len(news['likes'])})", key=f"like_{news['id']}"):
#             user = "ТестовыйНик"
#             if user not in news['likes']:
#                 news['likes'].append(user)
#                 if user in news['dislikes']:
#                     news['dislikes'].remove(user)
#     with col2:
#         if st.button(f"👎 Дизлайк ({len(news['dislikes'])})", key=f"dislike_{news['id']}"):
#             user = "ТестовыйНик"
#             if user not in news['dislikes']:
#                 news['dislikes'].append(user)
#                 if user in news['likes']:
#                     news['likes'].remove(user)

#     # Имена лайкнувших и дизлайкнувших
#     st.write("Лайкнули:", ", ".join(news['likes']))
#     st.write("Дизлайкнули:", ", ".join(news['dislikes']))

#     # Комментарии
#     st.subheader("Комментарии")
#     for c in news['comments']:
#         c_cols = st.columns([1, 5])
#         with c_cols[0]:
#             st.image(c['avatar'], width=30)
#         with c_cols[1]:
#             st.write(f"**{c['nick']}**: {c['text']}")

#     # Кнопки редактирования/удаления (условно, автор или мастер)
#     if st.button(f"Редактировать (id={news['id']})"):
#         st.info("Редактирование пока не реализовано")
#     if st.button(f"Удалить (id={news['id']})"):
#         news['status'] = "Неактуален"
#         st.success("Новость скрыта")


st.sidebar.title("Меню")
if name:
    st.sidebar.caption(f"Пользователь: {name}")
authenticator.logout("Выйти", location="sidebar", key="Logout", use_container_width=True)
section = st.sidebar.radio("Выберите раздел:", ["Профиль", "Новости"])

if section == "Профиль":
    Profile()
#elif section == "Новости":
#    News() 

