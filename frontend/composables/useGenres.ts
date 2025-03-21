export function useGenres() {
  const genres = ref([
    'Action', 'Anime', 'Comedies', 'Documentaries',
    'Drama', 'Fantasy', 'Horror', 'International',
    'Kids & Family', 'Romance', 'Sci-Fi', 'Thriller'
  ])

  const selectedGenres = ref<string[]>([])

  function toggleGenre(genre: string) {
    if (selectedGenres.value.includes(genre)) {
      selectedGenres.value = selectedGenres.value.filter(g => g !== genre)
    } else {
      selectedGenres.value.push(genre)
    }
  }

  return { genres, selectedGenres, toggleGenre }
}