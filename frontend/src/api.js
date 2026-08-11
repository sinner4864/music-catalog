const jsonHeaders = { 'Content-Type': 'application/json' }

export async function request(path, options = {}) {
  const response = await fetch(`/api${path}`, { ...options, headers: { ...jsonHeaders, ...options.headers } })
  if (response.status === 204) return null
  const data = await response.json()
  if (!response.ok) {
    const message = Object.values(data).flat().join(' ') || 'Не удалось выполнить запрос.'
    throw new Error(message)
  }
  return data
}

