import streamlit as st
from datetime import datetime
import pandas as pd
import base64
from api.backend_api import APIClient
import streamlit_authenticator as stauth
import hashlib
import yaml
import random
from pathlib import Path

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


_hashed_any = _maybe_hash_passwords_inplace(config)
authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )

api = APIClient("http://localhost:8000")

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
        character = {
            "photo": "https://i.imgur.com/Z7AzH2c.png",  # можно заменить на ссылку
            "name": "Альдрик ван Хольц",
            "alt_names": "Серый Философ, Старший Шепот",
            "player_name": "Константин Л.",
            "shreknet": "@philosopher_13",
            "status": "Активен",        # или "Торпор"
            "is_torpor": False,          # включи True — появится кнопка выхода
        "disciplines": {
                "Доминирование": [
                    {
                        "name": "Взгляд хищника",
                        "level": 1,
                        "description": "Цель ощущает давление воли персонажа.",
                    },
                    {
                        "name": "Команда",
                        "level": 2,
                        "description": "Краткий приказ, которому сложно сопротивляться.",
                    },
                ],
                "Стойкость": [
                    {
                        "name": "Каменная плоть",
                        "level": 1,
                        "description": "Тело становится устойчивее к урону.",
                    }
                ],
            },
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

        stats = {
            "clan": "Тремер",
            "clan_hint": "Кровавые маги. Строгая пирамида, дисциплины: Тауматургия, Ауспекс, Доминирование.",

            "sir": "Магистр Рудольф Гельман",
            "sir_hint": "Старший оккультист Венского Чанцери.",

            "generation_base": 10,
            "generation_mod": -1,

            "health": 2,   # 0–6
            "health_hint": "Каждый уровень — один шаг к торпору. При 6 — торпор.",  # 0–10

            "hunger": 4,

            "str_base": 2,
            "str_mod": 1,

            "sta_base": 3,
            "sta_mod": 0,

            "ritualist": True,
            "evade": False,
            "true_faith": False,
            "infernalist": False,

            "extra_status": "Допуск в закрытый ритуальный круг.",

            "torpor_button": True,       # кнопка “Впасть в торпор”
            "diablerie_hint": "Диаблери — тяжёлое преступление. Последствия определяет мастер."
        }

        if "hunger_value" not in st.session_state:
            st.session_state.hunger_value = stats["hunger"]

        @st.dialog("Клан")
        def modal_clan():
            st.write(stats["clan_hint"])

        @st.dialog("Сир")
        def modal_sire():
            st.write(stats["sir_hint"])

        @st.dialog("Здоровье")
        def modal_health():
            st.write(stats["health_hint"])

        @st.dialog("Диаблери")
        def modal_diablerie():
            st.write(stats["diablerie_hint"])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Клан")
            st.write(f"**{stats['clan']}**")
            st.button("Подсказка", key="clan_hint_btn", on_click=modal_clan)

        with col2:
            st.subheader("Сир")
            st.write(f"**{stats['sir']}**")
            st.button("Подсказка", key="sir_hint_btn", on_click=modal_sire)

        with col3:
            st.subheader("Поколение")
            gen = stats["generation_base"] + stats["generation_mod"]
            st.metric("Генерация", gen)
            st.caption(f"База: {stats['generation_base']}  |  Модификатор: {stats['generation_mod']}")

        st.markdown("---")

        # ---------------------------- Здоровье / Голод ----------------------------

        st.subheader("Основные ресурсы")

        colA, colB = st.columns(2)

        with colA:
            st.metric("Здоровье", f"{stats['health']} / 6")
            st.button("Что это?", key="health_hint_btn", on_click=modal_health)

        with colB:
            st.metric("Голод", f"{st.session_state.hunger_value} / 10")
            col_minus, col_plus = st.columns([1, 1])
            with col_minus:
                if st.button('minus', key="hunger_minus"):
                    st.session_state.hunger_value = max(0, st.session_state.hunger_value - 1)
                    st.rerun()
            with col_plus:
                if st.button('plus', key="hunger_plus"):
                    st.session_state.hunger_value = min(10, st.session_state.hunger_value + 1)
                    st.rerun()

        # ---------------------------- Сила / Стамина ----------------------------

        st.subheader("Физические параметры")

        colX, colY = st.columns(2)

        with colX:
            st.metric(
                "Сила",
                value=stats["str_base"] + stats["str_mod"],
                delta=f"+{stats['str_mod']} мод."
            )
            st.caption(f"База: {stats['str_base']}")

        with colY:
            st.metric(
                "Стамина",
                value=stats["sta_base"] + stats["sta_mod"],
                delta=f"+{stats['sta_mod']} мод."
            )
            st.caption(f"База: {stats['sta_base']}")

        # ---------------------------- Флаги ----------------------------

        st.subheader("Статусные флаги")

        colF1, colF2, colF3, colF4 = st.columns(4)

        with colF1:
            st.checkbox("Ритуалист", stats["ritualist"], disabled=True)

        with colF2:
            st.checkbox("Уворот", stats["evade"], disabled=True)

        with colF3:
            st.checkbox("Истинная вера", stats["true_faith"], disabled=True)

        with colF4:
            st.checkbox("Ощущается инферналистом", stats["infernalist"], disabled=True)

        # ---------------------------- Другие статусы ----------------------------

        st.subheader("Другие статусы")
        st.info(stats["extra_status"])

        # ---------------------------- Кнопки ----------------------------

        st.markdown("### Системные действия")

        if stats["torpor_button"]:
            st.button("⚰️ Впасть в торпор (фиксировано)", use_container_width=True)

        st.button("Меня диаблерят", use_container_width=True, on_click=modal_diablerie)

        # ДОПОЛНЕНИЕ: БЛОКИ 3–5 (Streamlit, совместимо с @st.dialog)
        # ВСТАВЛЯТЬ В КОНЕЦ ФАЙЛА ПОСЛЕ БЛОКА 2

        # =========================================================
        # БЛОК 3 — ДИСЦИПЛИНЫ
        # =========================================================

        st.divider()
        st.header("Дисциплины")

        @st.dialog("Способность")
        def ability_dialog(name, discipline, level, description):
            st.markdown(f"""
        **Название:** {name}  
        **Дисциплина:** {discipline}  
        **Уровень:** {level}
        
        {description}
        """)

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

def library():
    ss = st.session_state
    if "library_page" not in ss:
        ss.library_page = "list_of_all_items"
        ss.item = {}
    def list_of_all_items():
        items = api.get_library()

        if st.button("Создать статью"):
            ss.library_page = "create_library_item"
            st.rerun()

        st.title("📚 Библиотека")

        if not items:
            st.info("Статей нет")
        else:
            cols = st.columns(3)

            for i, article in enumerate(items):
                print(article)
                with cols[i % 3]:
                    with st.container(border=True):
                        st.subheader(article.get("name") or "Без названия")
                        st.caption(f'Тип: {article.get("item_type")}')
                        try:
                            st.image(base64.b64decode(article["picture"]), caption="Загруженное изображение",
                                     use_container_width=True)
                        except:
                            pass
                        if st.button("Открыть полностью", key=article.get("_id")):
                            ss.library_page = "full_version_of_item"
                            ss.item = article
                            st.rerun()
    def full_version_of_item(article):

        if st.button("⬅ Назад"):
            ss.library_page = "list_of_all_items"
            st.rerun()

        st.title(article.get("name") or "Без названия")
        st.caption(
            f'{article.get("item_type")} • '
            f'{article.get("author")} • '
            f'{article.get("date")}'
        )

        try:
            st.image(
                base64.b64decode(article["picture"]),
                caption="Загруженное изображение",
                use_container_width=False
            )
        except:
            pass

        st.divider()
        st.write(article.get("item_text") or "_Текст отсутствует_")
        st.divider()
        if st.button("Редактировать"):
            ss.library_page = "edit"
            st.rerun()
    def edit():
        article = ss.item
        if st.button("⬅ Отмена"):
            ss.library_page = "full_version_of_item"
            st.rerun()
        st.title("Редактирование статьи")

        title = st.text_input("Название", article["name"])

        type_ = st.selectbox(
            "Тип",
            ["Lore", "Game text", "Rule"],
            ["Lore", "Game text", "Rule"].index(article["item_type"])
        )

        access = st.selectbox(
            "Доступ",
            ['Player', 'Game technician', 'Macronosphere', 'Master'],
            ['Player', 'Game technician', 'Macronosphere', 'Master'].index(article["access"])
        )

        text = st.text_area(
            "Полный текст",
            article["item_text"],
            height=400
        )
        picture = st.file_uploader(
            "Выберите изображение",
            type=["png", "jpg", "jpeg", "webp"],
        )
        if picture:
            based_picture = base64.b64encode(picture.getvalue()).decode('utf-8')
        else:
            based_picture = None
        if st.button("Сохранить"):
            api.edit_library_item(article["_id"], title, type_, text, access, based_picture)
            ss.library_page = "list_of_all_items"
            st.rerun()
    def create_library_item():
        st.title("Создание статьи")

        title = st.text_input("Название")

        type_ = st.selectbox(
            "Тип",
            ["Lore", "Game text", "Rule"]
        )

        access = st.selectbox(
            "Доступ",
            ['Player', 'Game technician', 'Macronosphere', 'Master']
        )

        text = st.text_area(
            "Полный текст",
            height=400
        )
        picture = st.file_uploader(
            "Выберите изображение",
            type=["png", "jpg", "jpeg", "webp"]
        )
        if st.button("Сохранить"):
            api.create_library_item(title, type_, text, str(datetime.now()), access, "Aboba",
                                    base64.b64encode(picture.getvalue()).decode('utf-8'))

    current_user = {
        "name": "Альдрик ван Хольц",
        "role": "Master",  # Игрок | Мастер | Игротех | Макроносфер
    }

    if ss.library_page == "list_of_all_items":
        list_of_all_items()
    elif ss.library_page == "full_version_of_item":
        full_version_of_item(ss.item)
    elif ss.library_page == "edit":
        edit()
    elif ss.library_page == "create_library_item":
        create_library_item()


def character_gallery():
    pass

st.sidebar.title("Меню")
if name:
    st.sidebar.caption(f"Пользователь: {name}")
authenticator.logout("Выйти", location="sidebar", key="Logout", use_container_width=True)
section = st.sidebar.radio("Выберите раздел:", ["Профиль", "Новости"])
section = st.sidebar.radio("Выберите раздел:", ["Профиль", "Новости", "Библиотека", "Создать статью",  "Галерея персонажей"])

if section == "Профиль":
    Profile()
elif section == "Библиотека":
    library()
elif section == "Галерея персонажей":
    character_gallery()
#elif section == "Новости":
#    News()
