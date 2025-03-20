<script setup lang="ts">
import type { FormSubmitEvent, FormError } from '@nuxt/ui'

// État réactif du formulaire
const state = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// Fonction de validation sans librairie externe
const validate = (state: any): FormError[] => {
  const errors: FormError[] = []

  if (!state.name) {
    errors.push({ name: 'name', message: 'Name is required' })
  }

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

  if (state.password !== state.confirmPassword) {
    errors.push({ name: 'confirmPassword', message: 'Passwords do not match' })
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
    const response = await $api.post('/auth/register', {
      name: state.name,
      email: state.email,
      password: state.password
    })

    toast.add({ title: 'Registration Successful', description: 'Redirecting to login...', color: 'success' })

    setTimeout(() => {
      navigateTo('/auth/login')
    }, 1500)
  } catch (error) {
    toast.add({ title: 'Error', description: 'Registration failed', color: 'error' })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <UCard class="max-w-md mx-auto mt-10">
    <template #header>
      <h2 class="text-xl font-semibold text-center">Sign Up</h2>
    </template>

    <UForm :validate="validate" :state="state" class="space-y-4" @submit="onSubmit">
      <UFormField label="Full Name" name="name">
        <UInput v-model="state.name" placeholder="Enter your full name" />
      </UFormField>

      <UFormField label="Email" name="email">
        <UInput v-model="state.email" placeholder="Enter your email" />
      </UFormField>

      <UFormField label="Password" name="password">
        <UInput v-model="state.password" type="password" placeholder="Enter your password" />
      </UFormField>

      <UFormField label="Confirm Password" name="confirmPassword">
        <UInput v-model="state.confirmPassword" type="password" placeholder="Confirm your password" />
      </UFormField>

      <UButton type="submit" block :loading="loading">
        Sign Up
      </UButton>

      <p class="text-sm text-center">
        Already have an account? <NuxtLink to="/auth/login" class="text-primary">Sign in</NuxtLink>
      </p>
    </UForm>
  </UCard>
</template>