import { afterEach, describe, expect, it, vi } from 'vitest'
import { request } from './api'

afterEach(() => vi.restoreAllMocks())

describe('request', () => {
  it('returns parsed JSON for a successful response', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => ({ id: 1 }) }))
    await expect(request('/albums/')).resolves.toEqual({ id: 1 })
  })

  it('turns API validation details into an Error', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 400, json: async () => ({ title: ['Обязательное поле.'] }) }))
    await expect(request('/albums/')).rejects.toThrow('Обязательное поле.')
  })
})

