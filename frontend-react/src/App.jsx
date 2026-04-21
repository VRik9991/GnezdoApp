import { useEffect, useState } from 'react'
import './App.css'
import Sidebar from './components/Sidebar'
import Button from './components/Button'
import CheckBox from './components/CheckBox'
import Text from './components/Text'
import Hint from './components/Hint'
import clansData from '../../backend/data/clans.json'
import disciplinesData from '../../backend/data/disciplines.json'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const SESSION_KEY = 'gnezdo-active-email'
const PROFILE_TABS = [{ id: 'profile', label: 'Профиль' }]

const DEFAULT_CHARACTER = {
  morality: {
    humanity: 7,
    feeding: 'Согласованное',
    beastImage: 'Голодный волк',
    principles: [
      { name: 'Не убивать невинных', pillar: 'Сострадание' },
      { name: 'Держать слово', pillar: 'Честь' },
    ],
  },
  resources: {
    heartDew: 12,
    materials: 340,
    territories: [
      { name: 'Старый порт', status: 'Под контролем' },
      { name: 'Северный рынок', status: 'Оспаривается' },
    ],
  },
}

function normalizeClan(value) {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replaceAll('_', ' ')
    .replaceAll('-', ' ')
}

function normalizeTranslationKey(value) {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
}

function collectTranslations() {
  const disciplineMap = new Map()
  const powerMap = new Map()

  function store(map, enValue, ruValue) {
    const en = String(enValue || '').trim()
    const ru = String(ruValue || '').trim()
    if (!en || !ru) {
      return
    }

    map.set(en, ru)
    map.set(en.toLowerCase(), ru)

    const normalized = normalizeTranslationKey(en)
    if (normalized) {
      map.set(normalized, ru)
    }
  }

  for (const clan of clansData.clans || []) {
    for (const discipline of clan.dis || []) {
      store(disciplineMap, discipline.en, discipline.ru)
    }
  }

  for (const discipline of disciplinesData.disciplines || []) {
    store(disciplineMap, discipline?.name?.en, discipline?.name?.ru)

    for (const power of discipline?.['поддисциплины'] || []) {
      store(powerMap, power?.name?.en, power?.name?.ru)
    }
  }

  return { disciplineMap, powerMap }
}

const { disciplineMap, powerMap } = collectTranslations()

function getTranslation(map, value) {
  const raw = String(value || '').trim()
  if (!raw) {
    return ''
  }

  return map.get(raw) || map.get(raw.toLowerCase()) || map.get(normalizeTranslationKey(raw)) || ''
}

function resolveClanName(clanValue) {
  const normalized = normalizeClan(clanValue)
  const clan = (clansData.clans || []).find((item) => {
    const en = normalizeClan(item.en)
    const ru = normalizeClan(item.ru)
    return normalized && (normalized === en || normalized === ru)
  })

  if (clan) {
    return clan.ru || clan.en
  }

  return clanValue || 'Неизвестный клан'
}

function buildDisciplinesMap(stats) {
  const grouped = {}

  for (const item of stats?.disciplines || []) {
    const disciplineName =
      getTranslation(disciplineMap, item.discipline_en) ||
      item.discipline_en ||
      'Неизвестная дисциплина'
    const powerName =
      getTranslation(powerMap, item.power_en) || item.power_en || 'Неизвестная способность'

    if (!grouped[disciplineName]) {
      grouped[disciplineName] = []
    }

    grouped[disciplineName].push({
      name: powerName,
      level: item.level || 0,
      description: item.description || 'Описание пока отсутствует.',
    })
  }

  return grouped
}

function buildCharacter(user) {
  const stats = user?.stats || {}

  return {
    photo: user?.foto || 'https://placehold.co/460x620/120f10/d7d0cb?text=Gnezdo',
    name: user?.character_name || 'Безымянный персонаж',
    altNames: user?.other_character_name || 'Нет альтернативных имён',
    playerName: [user?.name, user?.last_name ? `${user.last_name[0]}.` : '']
      .filter(Boolean)
      .join(' '),
    shreknet: user?.tg_name || 'Не указан',
    status: user?.status || 'Активен',
    isTorpor: Boolean(stats?.is_torpor),
    clanDisplay: resolveClanName(stats?.clan),
    disciplines: buildDisciplinesMap(stats),
    morality: {
      humanity: stats?.humanity ?? DEFAULT_CHARACTER.morality.humanity,
      feeding: stats?.feeding || DEFAULT_CHARACTER.morality.feeding,
      beastImage: stats?.beast_image || DEFAULT_CHARACTER.morality.beastImage,
      principles: stats?.principles || DEFAULT_CHARACTER.morality.principles,
    },
    resources: {
      heartDew: stats?.heart_dew ?? DEFAULT_CHARACTER.resources.heartDew,
      materials: stats?.materials ?? DEFAULT_CHARACTER.resources.materials,
      territories: stats?.territories || DEFAULT_CHARACTER.resources.territories,
    },
  }
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }

  return response.json()
}

function isPasswordValid(inputPassword, storedPassword) {
  const plainInput = String(inputPassword || '')
  const stored = String(storedPassword || '')

  if (!plainInput || !stored) {
    return false
  }

  return plainInput === stored
}

function App() {
  const [activeTab, setActiveTab] = useState('profile')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [user, setUser] = useState(null)
  const [authError, setAuthError] = useState('')
  const [loading, setLoading] = useState(false)
  const [actionMessage, setActionMessage] = useState('')
  const [principleTimers, setPrincipleTimers] = useState({})

  useEffect(() => {
    const storedEmail = window.sessionStorage.getItem(SESSION_KEY)
    if (!storedEmail) {
      return
    }

    setEmail(storedEmail)
    setLoading(true)

    apiRequest(`/user?email=${encodeURIComponent(storedEmail)}`)
      .then((payload) => {
        setUser(payload)
        setAuthError('')
      })
      .catch(() => {
        window.sessionStorage.removeItem(SESSION_KEY)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  async function handleLogin(event) {
    event.preventDefault()
    setLoading(true)
    setAuthError('')
    setActionMessage('')

    try {
      const credentials = await apiRequest('/user_credentials')
      const entry = credentials?.usernames?.[email]

      if (!entry || !isPasswordValid(password, entry.password)) {
        throw new Error('AUTH')
      }

      const payload = await apiRequest(`/user?email=${encodeURIComponent(email)}`)
      setUser(payload)
      window.sessionStorage.setItem(SESSION_KEY, email)
    } catch (caughtError) {
      setUser(null)
      setAuthError(
        caughtError.message === 'AUTH'
          ? 'Неверный логин или пароль.'
          : 'Не удалось подключиться к API. Проверьте backend на http://localhost:8000.',
      )
    } finally {
      setLoading(false)
    }
  }

  function handleLogout() {
    setUser(null)
    setPassword('')
    setActiveTab('profile')
    setActionMessage('')
    window.sessionStorage.removeItem(SESSION_KEY)
  }

  async function updateUserStats(nextStats) {
    if (!user) {
      return
    }

    const nextUser = { ...user, stats: nextStats }
    setUser(nextUser)

    try {
      const savedUser = await apiRequest('/user', {
        method: 'PUT',
        body: JSON.stringify(nextUser),
      })

      setUser(savedUser)
    } catch {
      setUser(user)
      setActionMessage('Не удалось сохранить изменения на сервере.')
    }
  }

  async function handleHungerChange(delta) {
    if (!user?.stats) {
      return
    }

    const currentValue = Number(user.stats.hunger || 0)
    const nextValue = Math.max(0, Math.min(10, currentValue + delta))
    if (nextValue === currentValue) {
      return
    }

    setActionMessage('')
    await updateUserStats({ ...user.stats, hunger: nextValue })
  }

  async function handleFlagToggle(flagName) {
    if (!user?.stats) {
      return
    }

    setActionMessage('')
    await updateUserStats({
      ...user.stats,
      [flagName]: !user.stats[flagName],
    })
  }

  function showAction(message) {
    setActionMessage(message)
  }

  function handlePrincipleDrop(index, type, label) {
    setPrincipleTimers((current) => ({
      ...current,
      [index]: type,
    }))

    setActionMessage(`${label} уронена. Запущен таймер.`)
  }

  const character = buildCharacter(user)
  const stats = user?.stats || {}
  const generation = Number(stats.generation || 0) + Number(stats.generation_mod || 0)
  const strength = Number(stats.strength || 0) + Number(stats.strength_mod || 0)
  const stamina = Number(stats.stamina || 0) + Number(stats.stamina_mod || 0)

  if (!user) {
    return (
      <main className="login-screen">
        <section className="login-panel">
          <Text as="p" variant="caption" className="login-panel__eyebrow">
            Gnezdo
          </Text>
          <Text as="h1" variant="lead" tone="strong" className="login-panel__title">
            Вход в приложение
          </Text>
          <Text className="login-panel__copy">
            React-версия фронтенда работает параллельно со Streamlit и использует тот же backend.
          </Text>

          <form className="login-form" onSubmit={handleLogin}>
            <label className="field">
              <Text variant="caption">Логин</Text>
              <input
                className="field__input"
                type="text"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="Введите что угодно"
                autoComplete="off"
              />
            </label>

            <label className="field">
              <Text variant="caption">Пароль</Text>
              <input
                className="field__input"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="Введите пароль"
                autoComplete="current-password"
              />
            </label>

            <Button type="submit" className="login-form__submit" disabled={loading}>
              {loading ? 'Вход...' : 'Открыть приложение'}
            </Button>
          </form>

          {authError ? (
            <Text className="status-banner status-banner--error">{authError}</Text>
          ) : null}
        </section>
      </main>
    )
  }

  return (
    <>
      <Sidebar
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        tabs={PROFILE_TABS}
        title={character.name}
      />

      <main className="page-shell app-layout">
        <header className="topbar">
          <div>
            <Text variant="caption" className="section-eyebrow">
              React Frontend
            </Text>
            <Text as="h1" variant="lead" tone="strong" className="page-title">
              {character.name}
            </Text>
            <Text>{character.playerName || 'Игрок не указан'}</Text>
          </div>

          <Button className="topbar-button" onClick={handleLogout}>
            Выйти
          </Button>
        </header>

        {actionMessage ? <Text className="status-banner">{actionMessage}</Text> : null}

        {activeTab === 'profile' ? (
          <section className="profile-grid">
            <article className="hero-card panel">
              <div className="hero-card__media">
                <img className="hero-card__image" src={character.photo} alt={character.name} />
              </div>

              <div className="hero-card__body">
                <Text variant="caption" className="section-eyebrow">
                  Персонаж
                </Text>
                <Text as="h2" variant="lead" tone="strong" className="card-title">
                  {character.name}
                </Text>
                <Text>Другие имена: {character.altNames}</Text>
                <Text>Игрок: {character.playerName || 'Не указан'}</Text>
                <Text>Шрекнет: {character.shreknet}</Text>
                <Text className={character.isTorpor ? 'hero-status hero-status--danger' : 'hero-status'}>
                  {character.isTorpor ? 'Персонаж в торпоре' : `Статус: ${character.status}`}
                </Text>

                <div className="action-column">
                  <Button
                    className="button-block"
                    onClick={() => showAction('Заявка сохранена как черновик.')}
                  >
                    Сделать заявку
                  </Button>
                  <Button
                    className="button-block"
                    onClick={() => showAction('Загрузка пока не подключена в React-версии.')}
                  >
                    Загрузка?
                  </Button>
                  {stats.torpor_button ? (
                    <Button
                      className="button-block"
                      onClick={() => showAction('Кнопка торпора пока переведена без серверной логики.')}
                    >
                      ⚰️ Впасть в торпор (фиксировано)
                    </Button>
                  ) : null}
                  {character.isTorpor ? (
                    <Button
                      className="button-block"
                      onClick={() => showAction('Выход из торпора пока не подключен к backend.')}
                    >
                      Выйти из торпора
                    </Button>
                  ) : null}
                </div>
              </div>
            </article>

            <section className="stats-overview">
              <article className="panel stat-card">
                <Text variant="caption" className="section-eyebrow">
                  Клан
                </Text>
                <Text as="h2" variant="lead" tone="strong" className="card-title">
                  {character.clanDisplay}
                </Text>
                  <Hint
                    buttonLabel="Подсказка"
                    title="Клан"
                    message={stats.clan_hint || 'Подсказка по клану пока отсутствует.'}
                    buttonClassName="secondary-button button-block"
                  />
              </article>

              <article className="panel stat-card">
                <Text variant="caption" className="section-eyebrow">
                  Сир
                </Text>
                <Text as="h2" variant="lead" tone="strong" className="card-title">
                  {stats.sir_name || 'Не указан'}
                </Text>
                  <Hint
                    buttonLabel="Подсказка"
                    title="Сир"
                    message={stats.sir_name_hint || 'Подсказка по сиру пока отсутствует.'}
                    buttonClassName="secondary-button button-block"
                  />
              </article>

              <article className="panel stat-card">
                <Text variant="caption" className="section-eyebrow">
                  Поколение
                </Text>
                <Text as="h2" variant="lead" tone="strong" className="metric-value">
                  {generation}
                </Text>
                <Text>
                  База: {stats.generation || 0} | Модификатор: {stats.generation_mod || 0}
                </Text>
              </article>
            </section>

            <section className="panel content-section">
              <div className="section-header">
                <div>
                  <Text variant="caption" className="section-eyebrow">
                    Основные ресурсы
                  </Text>
                  <Text as="h2" variant="lead" tone="strong" className="card-title">
                    Здоровье и голод
                  </Text>
                </div>
              </div>

              <div className="resource-grid">
                <article className="resource-card">
                  <Text variant="caption">Здоровье</Text>
                  <Text as="p" variant="lead" tone="strong" className="metric-value">
                    {stats.health || 0} / 6
                  </Text>
                  <Hint
                    buttonLabel="Что это?"
                    title="Здоровье"
                    message={stats.health_hint || 'Подсказка по здоровью пока отсутствует.'}
                    buttonClassName="secondary-button button-block"
                  />
                </article>

                <article className="resource-card">
                  <Text variant="caption">Голод</Text>
                  <Text as="p" variant="lead" tone="strong" className="metric-value">
                    {stats.hunger || 0} / 10
                  </Text>
                  <div className="compact-actions compact-actions--equal">
                    <Button className="button-block" onClick={() => handleHungerChange(-1)}>
                      minus
                    </Button>
                    <Button className="button-block" onClick={() => handleHungerChange(1)}>
                      plus
                    </Button>
                  </div>
                </article>
              </div>
            </section>

            <section className="panel content-section">
              <div className="section-header">
                <div>
                  <Text variant="caption" className="section-eyebrow">
                    Физические параметры
                  </Text>
                  <Text as="h2" variant="lead" tone="strong" className="card-title">
                    Сила и стамина
                  </Text>
                </div>
              </div>

              <div className="resource-grid">
                <article className="resource-card">
                  <Text variant="caption">Сила</Text>
                  <Text as="p" variant="lead" tone="strong" className="metric-value">
                    {strength}
                  </Text>
                  <Text>База: {stats.strength || 0}</Text>
                  <Text>Модификатор: +{stats.strength_mod || 0}</Text>
                </article>

                <article className="resource-card">
                  <Text variant="caption">Стамина</Text>
                  <Text as="p" variant="lead" tone="strong" className="metric-value">
                    {stamina}
                  </Text>
                  <Text>База: {stats.stamina || 0}</Text>
                  <Text>Модификатор: +{stats.stamina_mod || 0}</Text>
                </article>
              </div>
            </section>

            <section className="panel content-section">
              <div className="section-header">
                <div>
                  <Text variant="caption" className="section-eyebrow">
                    Статусные флаги
                  </Text>
                  <Text as="h2" variant="lead" tone="strong" className="card-title">
                    Системные метки
                  </Text>
                </div>
              </div>

              <div className="flags-grid">
                {[
                  ['ritualist', 'Ритуалист'],
                  ['dodge', 'Уворот'],
                  ['true_faith', 'Истинная вера'],
                  ['feels_infernalist', 'Ощущается инферналистом'],
                ].map(([flagName, label]) => (
                  <article key={label} className="flag-card">
                    <CheckBox
                      checked={Boolean(stats[flagName])}
                      label={label}
                      onToggle={() => handleFlagToggle(flagName)}
                    />
                    <Text>{label}</Text>
                  </article>
                ))}
              </div>

              <div className="info-box">
                <Text>{stats.extra_status || 'Дополнительные статусы отсутствуют.'}</Text>
              </div>

              <div className="action-column">
                <Button
                  className="button-block"
                  onClick={() => showAction('Кнопка заявки на диаблерию отмечена.')}
                >
                  Меня диаблерят
                </Button>
                <Hint
                  buttonLabel="Что значит диаблери?"
                  title="Диаблери"
                  message={stats.diablerie_hint || 'Подсказка по диаблери пока отсутствует.'}
                  buttonClassName="secondary-button button-block"
                />
              </div>
            </section>

            <section className="panel content-section">
              <div className="section-header">
                <div>
                  <Text variant="caption" className="section-eyebrow">
                    Дисциплины
                  </Text>
                  <Text as="h2" variant="lead" tone="strong" className="card-title">
                    Способности персонажа
                  </Text>
                </div>
              </div>

              <Button
                className="button-block"
                onClick={() => showAction('Заявка на изучение дисциплины сохранена как черновик.')}
              >
                ➕ Заявка на изучение дисциплины
              </Button>

              {Object.keys(character.disciplines).length ? (
                <div className="discipline-list">
                  {Object.entries(character.disciplines).map(([disciplineName, abilities]) => (
                    <article key={disciplineName} className="discipline-card">
                      <Text as="h3" variant="lead" tone="strong" className="discipline-title">
                        {disciplineName}
                      </Text>
                      <div className="discipline-abilities">
                        {abilities.map((ability, index) => (
                          <div key={`${disciplineName}-${index}`} className="discipline-ability">
                            <div>
                              <Text>{ability.name}</Text>
                              <Text>Уровень: {ability.level}</Text>
                            </div>
                            <Hint
                              buttonLabel="Инфо"
                              title={ability.name}
                              message={`${disciplineName}, уровень ${ability.level}. ${ability.description}`}
                              buttonClassName="secondary-button secondary-button--compact"
                            />
                          </div>
                        ))}
                      </div>
                    </article>
                  ))}
                </div>
              ) : (
                <Text>У персонажа пока нет отображаемых дисциплин.</Text>
              )}
            </section>

            <section className="panel content-section">
              <div className="section-header">
                <div>
                  <Text variant="caption" className="section-eyebrow">
                    Мораль
                  </Text>
                  <Text as="h2" variant="lead" tone="strong" className="card-title">
                    Человечность и принципы
                  </Text>
                </div>
              </div>

              <div className="resource-grid">
                <article className="resource-card">
                  <Text variant="caption">Человечность</Text>
                  <Text as="p" variant="lead" tone="strong" className="metric-value">
                    {character.morality.humanity}
                  </Text>
                  <Hint
                    buttonLabel="Инфо"
                    title="Человечность"
                    message="Отражает степень утраты человеческой природы."
                    buttonClassName="secondary-button button-block"
                  />
                </article>

                <article className="resource-card">
                  <Text variant="caption">Тип питания</Text>
                  <Text as="p" variant="lead" tone="strong" className="metric-value metric-value--small">
                    {character.morality.feeding}
                  </Text>
                  <Hint
                    buttonLabel="Инфо"
                    title="Тип питания"
                    message="Определяет допустимые способы утоления голода."
                    buttonClassName="secondary-button button-block"
                  />
                </article>
              </div>

              <div className="info-box">
                <Text>Образ зверя: {character.morality.beastImage}</Text>
              </div>

              <div className="principles-list">
                {character.morality.principles.map((principle, index) => (
                  <article key={`${principle.name}-${index}`} className="principle-card">
                    <Text>
                      {principle.name} — опора: {principle.pillar}
                    </Text>
                    {principleTimers[index] ? (
                      <Text className="status-banner status-banner--warning">
                        Таймер активен: {principleTimers[index] === 'principle' ? 'уронен принцип' : 'уронена опора'}
                      </Text>
                    ) : null}
                    <div className="compact-actions compact-actions--equal">
                      <Button
                        className="button-block"
                        onClick={() => handlePrincipleDrop(index, 'principle', 'Принцип')}
                      >
                        ⬇️ Принцип
                      </Button>
                      <Button
                        className="button-block"
                        onClick={() => handlePrincipleDrop(index, 'pillar', 'Опора')}
                      >
                        ⬇️ Опора
                      </Button>
                    </div>
                  </article>
                ))}
              </div>

              <Button
                className="button-block"
                onClick={() => showAction('Предзаполненная заявка на добавление принципа отмечена.')}
              >
                ➕ Добавить принцип
              </Button>
            </section>

            <section className="panel content-section">
              <div className="section-header">
                <div>
                  <Text variant="caption" className="section-eyebrow">
                    Накопления
                  </Text>
                  <Text as="h2" variant="lead" tone="strong" className="card-title">
                    Ресурсы и территории
                  </Text>
                </div>
              </div>

              <div className="resource-grid">
                <article className="resource-card">
                  <Text variant="caption">Сердечная роса</Text>
                  <Text as="p" variant="lead" tone="strong" className="metric-value">
                    {character.resources.heartDew}
                  </Text>
                </article>

                <article className="resource-card">
                  <Text variant="caption">Ресурсы</Text>
                  <Text as="p" variant="lead" tone="strong" className="metric-value">
                    {character.resources.materials}
                  </Text>
                </article>
              </div>

              <div className="territory-list">
                {character.resources.territories.map((territory, index) => (
                  <Hint
                    key={`${territory.name}-${index}`}
                    buttonLabel={`${territory.name} — ${territory.status}`}
                    title={territory.name}
                    message={`Статус территории: ${territory.status}`}
                    buttonClassName="territory-button button-block"
                  />
                ))}
              </div>
            </section>
          </section>
        ) : null}

        {/*
        <section className="panel news-panel">
          Новости временно закомментированы по запросу.
        </section>
        */}
      </main>
    </>
  )
}

export default App
