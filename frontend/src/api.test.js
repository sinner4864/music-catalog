import { afterEach, describe, expect, it, vi } from 'vitest'
import { request } from './api'

afterEach(() => vi.restoreAllMocks())

describe('request', () => {
  it('returns parsed JSON for a successful response', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      headers: { get: () => 'application/json' },
      json: async () => ({ id: 1 })
    }))
    await expect(request('/albums/')).resolves.toEqual({ id: 1 })
  })

  it('turns API validation details into an Error', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      status: 400,
      headers: { get: () => 'application/json' },
      json: async () => ({ title: ['Обязательное поле.'] })
    }))
    await expect(request('/albums/')).rejects.toThrow('Обязательное поле.')
  })

  it('returns a useful message for a network failure', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')))
    await expect(request('/albums/')).rejects.toThrow('Сервер недоступен')
  })

  it('handles a non-JSON server error', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      status: 502,
      headers: { get: () => 'text/html' },
      text: async () => 'Bad Gateway'
    }))
    await expect(request('/albums/')).rejects.toThrow('Bad Gateway')
  })
})
