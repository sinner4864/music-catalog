import { defineStore } from 'pinia'
import { request } from './api'

export const useCatalogStore = defineStore('catalog', {
  state: () => ({ albums: [], artists: [], loading: false, error: '', search: '', requestId: 0 }),
  actions: {
    async load(search = this.search) {
      this.search = search
      const requestId = ++this.requestId
      this.loading = true; this.error = ''
      try {
        const [albums, artists] = await Promise.all([
          request(`/albums/${search ? `?search=${encodeURIComponent(search)}` : ''}`), request('/artists/')
        ])
        if (requestId === this.requestId) [this.albums, this.artists] = [albums, artists]
      } catch (error) {
        if (requestId === this.requestId) this.error = error.message
      } finally {
        if (requestId === this.requestId) this.loading = false
      }
    },
    async createArtist(name) { await request('/artists/', { method: 'POST', body: JSON.stringify({ name }) }); await this.load(this.search) },
    async createAlbum(album) { await request('/albums/', { method: 'POST', body: JSON.stringify(album) }); await this.load(this.search) },
    async addTrack(albumId, track) { await request(`/albums/${albumId}/tracks/`, { method: 'POST', body: JSON.stringify(track) }); await this.load(this.search) },
    async removeTrack(albumId, trackId) { await request(`/albums/${albumId}/tracks/${trackId}/`, { method: 'DELETE' }); await this.load(this.search) },
    async removeAlbum(id) { await request(`/albums/${id}/`, { method: 'DELETE' }); await this.load(this.search) }
  }
})
