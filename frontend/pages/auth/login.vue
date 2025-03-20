<script setup lang="ts">
import type { FormSubmitEvent, FormError } from '@nuxt/ui'
import { useUserStore } from '~/store/userStore'

const userStore = useUserStore()
definePageMeta({
  middleware: 'guest',
  layout: 'auth'
})

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
  loading.value = true;

  try {
    const formData = new URLSearchParams();
    formData.append("username", state.email.trim());
    formData.append("password", state.password);

    const response = await fetch("http://localhost:8000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Login failed. Please try again.");
    }

    // Stocker manuellement le token dans Nuxt Auth
    const token = useCookie('auth.token')
    token.value = data.access_token

    userStore.login({
      id: data.id,
      email: data.email,
      username: data.username,
    });

    // Vérifier `first_login` et rediriger
    if (data.first_login) {
      navigateTo('/onboarding/actors') // Redirection vers l'onboarding
    } else {
      navigateTo('/dashboard')
    }

  } catch (error: any) {
    console.error("Erreur de connexion :", error);
    toast.add({ title: "Error", description: error.message || "Login failed", color: "error" });

  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <UCard class="max-w-md mx-auto mt-10">
    <template #header>
      <h2 class="text-xl font-semibold text-center">Sign In</h2>
    </template>

    <UForm :validate="validate" :state="state" class="space-y-4" @submit="onSubmit">
      <UFormField label="Email" name="username">
        <UInput v-model="state.email" placeholder="Enter your email" />
      </UFormField>

      <UFormField label="Password" name="password">
        <UInput v-model="state.password" type="password" placeholder="Enter your password" />
      </UFormField>

      <UButton type="submit" block :loading="loading">
        Sign In
      </UButton>
    </UForm>
    <p>Pas encore de compte ? <NuxtLink to="/auth/register">Inscris-toi ici</NuxtLink>
    </p>
  </UCard>
</template>