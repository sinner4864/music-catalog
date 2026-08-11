const jsonHeaders = { 'Content-Type': 'application/json' }

function flattenErrors(value) {
  if (Array.isArray(value)) return value.flatMap(flattenErrors)
  if (value && typeof value === 'object') return Object.values(value).flatMap(flattenErrors)
  return value == null ? [] : [String(value)]
}

export async function request(path, options = {}) {
  let response
  try {
    response = await fetch(`/api${path}`, {
      ...options,
      headers: { ...jsonHeaders, ...options.headers }
    })
  } catch {
    throw new Error('Сервер недоступен. Проверьте подключение и повторите попытку.')
  }

  if (response.status === 204) return null

  const contentType = response.headers?.get?.('content-type') || ''
  const data = contentType.includes('application/json')
    ? await response.json()
    : { detail: await response.text() }

  if (!response.ok) {
    const message = flattenErrors(data).join(' ') || 'Не удалось выполнить запрос.'
    throw new Error(message)
  }
  return data
}
