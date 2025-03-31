export function useGenres() {
  const genres = ref([
    'Action', ' Adventure', 'Animation', 'Crime', 'Children', 'Comedy', 'Documentary',
    'Drama', 'Fantasy', 'Horror', ' IMAX', 'International', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
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