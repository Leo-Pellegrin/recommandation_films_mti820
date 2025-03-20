<script setup lang="ts">
import type { FormSubmitEvent, FormError } from '@nuxt/ui'

definePageMeta({
  layout: 'auth'
})

// État réactif du formulaire
const state = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// Vérification des erreurs
const validate = (state: Record<string, string>): FormError[] => {
  const errors: FormError[] = []

  if (!state.name.trim()) errors.push({ name: 'name', message: 'Name is required' })

  if (!state.email.trim()) {
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

// Toast notifications & loading state
const toast = useToast()
const loading = ref(false)

// Fonction de soumission
async function onSubmit(event: FormSubmitEvent<any>) {
  loading.value = true

  try {
    if (state.password !== state.confirmPassword) {
      toast.add({ title: 'Error', description: 'Passwords do not match', color: 'error' })
      return
    }

    const response = await fetch("http://localhost:8000/api/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: state.name.trim(),
        email: state.email.trim(),
        password: state.password
      })
    })

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Registration failed. Please try again.");
    }

    if (data.id) {
      toast.add({ title: 'Success', description: 'Account created! Redirecting...', color: 'success' })
      setTimeout(() => {
        navigateTo('/auth/login')
      }, 1500);

    }

  } catch (error: any) {
    console.error('❌ Registration error:', error)
    let message = 'Registration failed. Please try again.'

    // Si l'API FastAPI renvoie un message d'erreur, on l'affiche
    if (error.message) {
      message = error.message
    }

    toast.add({ title: 'Error', description: message, color: 'error' })
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
        <UInput v-model="state.email" type="email" placeholder="Enter your email" />
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

    </UForm>
    <p class="text-sm text-center">
      Already have an account? <NuxtLink to="/auth/login" class="text-primary">Sign in</NuxtLink>
    </p>
  </UCard>
</template>