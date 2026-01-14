<!--
News Article Dialog Component

Displays full news article content when clicking on headlines.
-->
<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { ExternalLinkIcon } from 'lucide-vue-next'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

interface Props {
  articleUrl: string
  title: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
}>()

const isOpen = computed(() => !!props.articleUrl)
const isLoading = ref(false)
const articleContent = ref('')
const error = ref(null)

const fetchArticle = async () => {
  if (!props.articleUrl) return

  isLoading.value = true
  error.value = null

  try {
    // Try to fetch article content via backend proxy (to avoid CORS)
    const response = await axios.post(`${API_BASE}/api/v1/investment-engine/fetch-article`, {
      url: props.articleUrl
    }, {
      timeout: 10000 // 10 second timeout
    })

    if (response.data && response.data.content) {
      articleContent.value = response.data.content
    } else {
      throw new Error('No content returned')
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.message || 'Failed to fetch article'
    console.error('Error fetching article:', err)
  } finally {
    isLoading.value = false
  }
}

// Auto-fetch when dialog opens
const onOpenChange = (open: boolean) => {
  if (open && props.articleUrl) {
    fetchArticle()
  }
  if (!open) {
    emit('close')
  }
}
</script>

<template>
  <Dialog :open="isOpen" @update:open="onOpenChange">
    <DialogContent class="max-w-3xl max-h-[80vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle class="flex items-center justify-between gap-2">
          <span class="truncate flex-1">{{ title }}</span>
          <Button
            as="a"
            variant="outline"
            size="sm"
            :href="articleUrl"
            target="_blank"
            rel="noopener noreferrer"
          >
            <ExternalLinkIcon class="h-4 w-4 mr-2" />
            Open Original
          </Button>
        </DialogTitle>
        <DialogDescription v-if="isLoading">
          Loading article content...
        </DialogDescription>
      </DialogHeader>

      <div v-if="isLoading" class="py-8 text-center text-muted-foreground">
        <div class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto mb-4"></div>
        <p class="text-sm">Fetching article from Yahoo Finance...</p>
      </div>

      <div v-else-if="error" class="py-6">
        <div class="p-4 rounded-lg bg-destructive/10 text-destructive text-sm">
          <p class="font-medium mb-2">Failed to load article</p>
          <p class="text-xs">{{ error }}</p>
        </div>
        <div class="mt-4 flex gap-2">
          <Button
            variant="outline"
            size="sm"
            @click="fetchArticle"
          >
            Retry
          </Button>
          <Button
            as="a"
            size="sm"
            :href="articleUrl"
            target="_blank"
            rel="noopener noreferrer"
          >
            <ExternalLinkIcon class="h-4 w-4 mr-2" />
            Open on Yahoo Finance
          </Button>
        </div>
      </div>

      <div v-else-if="articleContent" class="prose prose-sm max-w-none">
        <div v-html="articleContent" class="article-content"></div>
      </div>
    </DialogContent>
  </Dialog>
</template>

<style scoped>
.article-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
}

.article-content :deep(p) {
  margin-bottom: 1rem;
  line-height: 1.75;
}

.article-content :deep(h2),
.article-content :deep(h3) {
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
}

.article-content :deep(a) {
  color: hsl(var(--primary));
  text-decoration: underline;
}

.article-content :deep(blockquote) {
  border-left: 4px solid hsl(var(--muted));
  padding-left: 1rem;
  font-style: italic;
  color: hsl(var(--muted-foreground));
}
</style>
