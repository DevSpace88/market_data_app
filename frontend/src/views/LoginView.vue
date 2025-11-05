// src/views/LoginView.vue
<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useToast } from '@/components/ui/toast/use-toast'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()
const authStore = useAuthStore()
const { toast } = useToast()

const username = ref('')
const password = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!username.value || !password.value) {
    toast({
      title: "Error",
      description: "Please fill in all fields",
      variant: "destructive",
    })
    return
  }

  loading.value = true
  const success = await authStore.login(username.value, password.value)
  loading.value = false

  if (success) {
    toast({
      title: "Success",
      description: "Successfully logged in",
    })
    // Redirect to intended page or dashboard
    const redirect = route.query.redirect || '/dashboard'
    router.push(redirect)
  } else {
    toast({
      title: "Error",
      description: authStore.error || "Login failed",
      variant: "destructive",
    })
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-background">
    <Card class="w-[350px]">
      <CardHeader>
        <CardTitle>Login</CardTitle>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div class="space-y-2">
            <Input
              v-model="username"
              type="text"
              placeholder="Username"
              required
            />
          </div>
          <div class="space-y-2">
            <Input
              v-model="password"
              type="password"
              placeholder="Password"
              required
            />
          </div>
          <Button
            type="submit"
            class="w-full"
            :disabled="loading"
          >
            {{ loading ? 'Loading...' : 'Login' }}
          </Button>
        </form>
        <Alert class="mt-4">
          <AlertDescription>
            <strong>Testdaten:</strong> Benutzername: <code>admin</code>, Passwort: <code>admin123</code>
          </AlertDescription>
        </Alert>
      </CardContent>
    </Card>
  </div>
</template>