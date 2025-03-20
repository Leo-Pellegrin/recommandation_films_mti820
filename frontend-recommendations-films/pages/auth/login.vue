<script setup lang="ts">
import type { FormSubmitEvent, FormError } from '@nuxt/ui'

// État réactif du formulaire
const state = reactive({
  email: '',
  password: ''
})

// Fonction de validation manuelle
const validate = (state: any): FormError[] => {
  const errors: FormError[] = []

  if (!state.email) {
    errors.push({ name: 'email', message: 'Email is required' })
  } else if (!/\S+@\S+\.\S+/.test(state.email)) {
    errors.push({ name: 'email', message: 'Invalid email format' })
  }

  if (!state.password) {
    errors.push({ name: 'password', message: 'Password is required' })
  } else if (state.password.length < 8) {
    errors.push({ name: 'password', message: 'Password must be at least 8 characters' })
  }

  return errors
}

// Toast notifications
const toast = useToast()
const loading = ref(false)

// Soumission du formulaire
async function onSubmit(event: FormSubmitEvent<any>) {
  loading.value = true
  try {
    const { $api } = useNuxtApp()
    const response = await $api.post('/auth/login', {
      email: state.email,
      password: state.password
    })

    localStorage.setItem('token', response.data.token)

    toast.add({ title: 'Login Successful', description: 'Redirecting...', color: 'success' })

    setTimeout(() => {
      navigateTo('/')
    }, 1500)
  } catch (error) {
    toast.add({ title: 'Error', description: 'Invalid credentials', color: 'error' })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <UCard class="max-w-md mx-auto mt-10">
    <template #header>
      <h2 class="text-xl font-semibold text-center">Sign In</h2>
    </template>

    <UForm :validate="validate" :state="state" class="space-y-4" @submit="onSubmit">
      <UFormField label="Email" name="email">
        <UInput v-model="state.email" placeholder="Enter your email" />
      </UFormField>

      <UFormField label="Password" name="password">
        <UInput v-model="state.password" type="password" placeholder="Enter your password" />
      </UFormField>

      <UButton type="submit" block :loading="loading">
        Sign In
      </UButton>
    </UForm>
  </UCard>
</template>