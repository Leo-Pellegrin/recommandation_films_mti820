<script setup lang="ts">
const form = ref({
  email: '',
  password: '',
  rememberMe: false
})

const login = async () => {
  try {
    // Appel API pour se connecter
    const { $api } = useNuxtApp()
    const response = await $api.post('/auth/login', form)
    console.log('Connexion réussie', response.data)
  } catch (error) {
    console.error('Erreur de connexion', error)
  }
}
</script>

<template>
  <div class="auth-container">
    <h1>Sign in</h1>
    <form @submit.prevent="login">
      <label>Email address</label>
      <input v-model="form.email" type="email" required />
      
      <label>Password</label>
      <input v-model="form.password" type="password" required />
      
      <div>
        <input v-model="form.rememberMe" type="checkbox" />
        <span>Remember me</span>
      </div>

      <button type="submit">Sign In</button>
      <p>Don't have an account? <NuxtLink to="/auth/register">Sign up here</NuxtLink></p>
    </form>
  </div>
</template>

<style scoped>
.auth-container {
  width: 300px;
  margin: auto;
  padding: 20px;
  background: #000;
  color: white;
}
</style>