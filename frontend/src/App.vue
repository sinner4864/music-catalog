<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useCatalogStore } from './store'

const store = useCatalogStore()
const search = ref('')
const artistName = ref('')
const album = reactive({ title: '', artist: '', release_year: new Date().getFullYear() })
const tracks = reactive({})
const flash = ref('')

async function perform(action, success) {
  store.error = ''; flash.value = ''
  try { await action(); flash.value = success } catch (error) { store.error = error.message }
}
async function addArtist() {
  await perform(() => store.createArtist(artistName.value), 'Исполнитель добавлен')
  if (!store.error) artistName.value = ''
}
async function addAlbum() {
  await perform(() => store.createAlbum(album), 'Альбом добавлен')
  if (!store.error) { album.title = ''; album.artist = '' }
}
async function addTrack(albumId) {
  const value = tracks[albumId]
  await perform(() => store.addTrack(albumId, { song_title: value.title, track_number: value.number }), 'Трек добавлен')
  if (!store.error) tracks[albumId] = { title: '', number: '' }
}
function trackDraft(id) { return tracks[id] ||= { title: '', number: '' } }
function confirmRemove(message, action) { if (window.confirm(message)) perform(action, 'Удалено') }
let timer
function applySearch() { clearTimeout(timer); timer = setTimeout(() => store.load(search.value), 250) }
onMounted(() => store.load())
</script>

<template>
  <main>
    <header>
      <div><span class="eyebrow">личная фонотека</span><h1>Needle<span>drop</span></h1></div>
      <p>Альбомы, которые хочется помнить.</p>
    </header>

    <section class="toolbar">
      <label class="search"><span>⌕</span><input v-model="search" @input="applySearch" placeholder="Альбом, исполнитель или песня" /></label>
      <div class="count">{{ store.albums.length }} {{ store.albums.length === 1 ? 'альбом' : 'альбомов' }}</div>
    </section>

    <div v-if="store.error" class="notice error">{{ store.error }}</div>
    <div v-if="flash" class="notice success">{{ flash }}</div>

    <section class="forms">
      <form @submit.prevent="addArtist">
        <h2>Новый исполнитель</h2>
        <input v-model="artistName" required maxlength="200" placeholder="Имя исполнителя" />
        <button>Добавить</button>
      </form>
      <form @submit.prevent="addAlbum">
        <h2>Новый альбом</h2>
        <input v-model="album.title" required maxlength="250" placeholder="Название" />
        <select v-model="album.artist" required><option disabled value="">Исполнитель</option><option v-for="artist in store.artists" :key="artist.id" :value="artist.id">{{ artist.name }}</option></select>
        <input v-model.number="album.release_year" required type="number" min="1900" :max="new Date().getFullYear()" aria-label="Год выпуска" />
        <button>Добавить</button>
      </form>
    </section>

    <div v-if="store.loading" class="empty">Загружаем пластинки…</div>
    <div v-else-if="!store.albums.length" class="empty">Здесь пока тихо. Добавьте первый альбом.</div>
    <section v-else class="grid">
      <article v-for="item in store.albums" :key="item.id" class="album-card">
        <button class="delete" title="Удалить альбом" @click="confirmRemove(`Удалить «${item.title}»?`, () => store.removeAlbum(item.id))">×</button>
        <div class="cover"><span>{{ item.artist_name.slice(0, 1) }}</span><i></i></div>
        <div class="album-info">
          <div class="year">{{ item.release_year }}</div><h2>{{ item.title }}</h2><h3>{{ item.artist_name }}</h3>
          <ol v-if="item.tracks.length">
            <li v-for="track in item.tracks" :key="track.id"><b>{{ String(track.track_number).padStart(2, '0') }}</b><span>{{ track.song.title }}</span><button title="Удалить трек" @click="confirmRemove('Удалить трек?', () => store.removeTrack(item.id, track.id))">×</button></li>
          </ol>
          <p v-else class="no-tracks">Трек-лист пока пуст</p>
          <form class="track-form" @submit.prevent="addTrack(item.id)">
            <input v-model="trackDraft(item.id).number" required type="number" min="1" placeholder="#" aria-label="Номер трека" />
            <input v-model="trackDraft(item.id).title" required maxlength="250" placeholder="Название песни" aria-label="Название песни" />
            <button title="Добавить трек">+</button>
          </form>
        </div>
      </article>
    </section>
  </main>
</template>

