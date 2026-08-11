import { defineStore } from 'pinia'
import { request } from './api'

export const useCatalogStore = defineStore('catalog', {
  state: () => ({ albums: [], artists: [], loading: false, error: '' }),
  actions: {
    async load(search = '') {
      this.loading = true; this.error = ''
      try {
        [this.albums, this.artists] = await Promise.all([
          request(`/albums/${search ? `?search=${encodeURIComponent(search)}` : ''}`), request('/artists/')
        ])
      } catch (error) { this.error = error.message } finally { this.loading = false }
    },
    async createArtist(name) { await request('/artists/', { method: 'POST', body: JSON.stringify({ name }) }); await this.load() },
    async createAlbum(album) { await request('/albums/', { method: 'POST', body: JSON.stringify(album) }); await this.load() },
    async addTrack(albumId, track) { await request(`/albums/${albumId}/tracks/`, { method: 'POST', body: JSON.stringify(track) }); await this.load() },
    async removeTrack(albumId, trackId) { await request(`/albums/${albumId}/tracks/${trackId}/`, { method: 'DELETE' }); await this.load() },
    async removeAlbum(id) { await request(`/albums/${id}/`, { method: 'DELETE' }); await this.load() }
  }
})

