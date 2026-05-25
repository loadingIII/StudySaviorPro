<template>
  <div class="knowledge-base">
    <!-- 头部区域 -->
    <div class="kb-header">
      <div class="kb-header-left">
        <button class="kb-back-btn" @click="$emit('close')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"/>
            <polyline points="12 19 5 12 12 5"/>
          </svg>
          <span>返回</span>
        </button>
        <div class="kb-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            <path d="M12 6l-4 4h8l-4 4"/>
          </svg>
        </div>
        <div class="kb-title-section">
          <h2 class="kb-title">知识库</h2>
          <p class="kb-subtitle">管理和查询您的文档知识</p>
        </div>
      </div>
    </div>

    <!-- 统计信息 -->
    <div class="kb-stats">
      <div class="stat-card">
        <div class="stat-value">{{ documents.length }}</div>
        <div class="stat-label">文档总数</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ formatSize(totalSize) }}</div>
        <div class="stat-label">存储空间</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ recentUploads }}</div>
        <div class="stat-label">本周上传</div>
      </div>
    </div>

    <!-- 操作栏 -->
    <div class="kb-actions">
      <div class="search-box">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索文档..."
          class="search-input"
        />
      </div>
      <button class="upload-btn" @click="triggerFileUpload">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <span>上传文档</span>
      </button>
      <input 
        ref="fileInput" 
        type="file" 
        multiple 
        accept=".pdf,.doc,.docx,.txt,.md"
        style="display: none"
        @change="handleFileChange"
      />
    </div>

    <!-- 文档列表 -->
    <div class="kb-content">
      <!-- 加载状态 -->
      <div v-if="isLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>正在加载文档...</p>
      </div>
      
      <!-- 错误提示 -->
      <div v-else-if="loadError" class="error-state">
        <div class="error-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </div>
        <h3>加载失败</h3>
        <p>{{ loadError }}</p>
        <button class="retry-btn" @click="fetchDocuments">重新加载</button>
      </div>
      
      <div v-else-if="filteredDocuments.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
        </div>
        <h3>{{ searchQuery ? '未找到匹配的文档' : '暂无文档' }}</h3>
        <p>{{ searchQuery ? '请尝试其他关键词搜索' : '点击上方"上传文档"按钮添加您的第一个文档' }}</p>
      </div>

      <div v-else class="document-list">
        <div 
          v-for="doc in filteredDocuments" 
          :key="doc.id"
          class="document-item"
          :class="{ uploading: doc.status === 'uploading', error: doc.status === 'error' }"
        >
          <div class="doc-icon" :class="getFileIconClass(doc.type)">
            <svg v-if="doc.type === 'pdf'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <path d="M9 13h6M9 17h6M9 9h1"/>
            </svg>
            <svg v-else-if="doc.type === 'word'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10 9 9 9 8 9"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10 9 9 9 8 9"/>
            </svg>
          </div>
          
          <div class="doc-info">
            <div class="doc-name">{{ doc.name }}</div>
            <div class="doc-meta">
              <span class="doc-type">{{ getFileTypeLabel(doc.type) }}</span>
              <span class="doc-size">{{ formatSize(doc.size) }}</span>
              <span class="doc-date">{{ formatDate(doc.uploadDate) }}</span>
            </div>
            <div v-if="doc.status === 'uploading'" class="upload-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: doc.progress + '%' }"></div>
              </div>
              <span class="progress-text">{{ doc.progress }}%</span>
            </div>
            <div v-if="doc.status === 'error'" class="upload-error">
              上传失败，请重试
            </div>
          </div>

          <div class="doc-actions">
            <button 
              class="doc-action-btn" 
              title="下载"
              @click="downloadDocument(doc)"
              :disabled="doc.status !== 'completed'"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              <span>下载</span>
            </button>
            <button 
              class="doc-action-btn delete" 
              title="删除"
              @click="confirmDelete(doc)"
              :disabled="doc.status === 'uploading'"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
              <span>删除</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="modal-content">
        <div class="modal-icon warning">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        </div>
        <h3>确认删除</h3>
        <p>确定要删除文档 "{{ documentToDelete?.name }}" 吗？此操作不可恢复。</p>
        <div class="modal-actions">
          <button class="modal-btn cancel" @click="showDeleteModal = false">取消</button>
          <button class="modal-btn confirm" @click="deleteDocument">删除</button>
        </div>
      </div>
    </div>

    <!-- 上传拖拽区域遮罩 -->
    <div 
      v-if="isDragging" 
      class="drag-overlay"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
    >
      <div class="drag-content">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <p>释放以上传文件</p>
      </div>
    </div>

    <!-- 文件上传加载画面 -->
    <div v-if="isUploading" class="upload-loading-overlay">
      <div class="upload-loading-content">
        <div class="upload-spinner-container">
          <div class="upload-spinner">
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
          </div>
          <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
        </div>
        <div class="upload-loading-text">
          <p class="upload-status">文件上传中，请稍候...</p>
          <p class="upload-filename">{{ uploadingFileName }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

// 后端返回的文件数据接口
interface FileVO {
  original_name: string
  file_size: number
  file_type: string
  created_at: string
}

// 前端文档接口
interface Document {
  id: string
  name: string
  type: string
  size: number
  uploadDate: Date
  status: 'uploading' | 'completed' | 'error'
  progress: number
  file?: File
}

const emit = defineEmits<{
  close: []
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const searchQuery = ref('')
const isDragging = ref(false)
const showDeleteModal = ref(false)
const documentToDelete = ref<Document | null>(null)
const isLoading = ref(false)
const loadError = ref('')
const isUploading = ref(false)
const uploadingFileName = ref('')

// 文档数据
const documents = ref<Document[]>([])

// 从后端获取文档列表
const fetchDocuments = async () => {
  isLoading.value = true
  loadError.value = ''
  try {
    const response = await fetch('/vector/add_documents')
    if (!response.ok) {
      throw new Error('获取文档列表失败')
    }
    const data: FileVO[] = await response.json()
    
    // 将后端数据转换为前端格式
    documents.value = data.map((file, index) => ({
      id: `doc_${index}_${Date.now()}`,
      name: file.original_name,
      type: getFileType(file.original_name),
      size: file.file_size,
      uploadDate: new Date(file.created_at),
      status: 'completed' as const,
      progress: 100
    }))
  } catch (error) {
    console.error('获取文档列表失败:', error)
    loadError.value = '获取文档列表失败，请稍后重试'
    // 使用默认数据作为回退
    documents.value = []
  } finally {
    isLoading.value = false
  }
}

// 计算属性
const filteredDocuments = computed(() => {
  if (!searchQuery.value) return documents.value
  const query = searchQuery.value.toLowerCase()
  return documents.value.filter(doc => 
    doc.name.toLowerCase().includes(query)
  )
})

const totalSize = computed(() => {
  return documents.value.reduce((sum, doc) => sum + doc.size, 0)
})

const recentUploads = computed(() => {
  const oneWeekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
  return documents.value.filter(doc => doc.uploadDate > oneWeekAgo).length
})

// 方法
const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (files) {
    Array.from(files).forEach(file => uploadFile(file))
  }
  // 重置 input 以便可以重复选择相同文件
  target.value = ''
}

const uploadFile = (file: File) => {
  isUploading.value = true
  uploadingFileName.value = file.name
  
  const fileType = getFileType(file.name)
  const newDoc: Document = {
    id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
    name: file.name,
    type: fileType,
    size: file.size,
    uploadDate: new Date(),
    status: 'uploading',
    progress: 0,
    file: file
  }
  
  documents.value.unshift(newDoc)
  
  const interval = setInterval(() => {
    const doc = documents.value.find(d => d.id === newDoc.id)
    if (doc && doc.status === 'uploading') {
      doc.progress += Math.random() * 30
      if (doc.progress >= 100) {
        doc.progress = 100
        doc.status = 'completed'
        clearInterval(interval)
        isUploading.value = false
        uploadingFileName.value = ''
      }
    }
  }, 500)
}

const getFileType = (filename: string): string => {
  const ext = filename.split('.').pop()?.toLowerCase() || ''
  if (ext === 'pdf') return 'pdf'
  if (['doc', 'docx'].includes(ext)) return 'word'
  if (['txt', 'md'].includes(ext)) return 'text'
  return 'other'
}

const getFileTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    pdf: 'PDF',
    word: 'Word',
    text: '文本',
    other: '其他'
  }
  return labels[type] || '其他'
}

const getFileIconClass = (type: string): string => {
  return `file-${type}`
}

const formatSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (date: Date): string => {
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) {
    const hours = Math.floor(diff / (1000 * 60 * 60))
    if (hours === 0) {
      const minutes = Math.floor(diff / (1000 * 60))
      return minutes <= 1 ? '刚刚' : `${minutes} 分钟前`
    }
    return `${hours} 小时前`
  } else if (days === 1) {
    return '昨天'
  } else if (days < 7) {
    return `${days} 天前`
  } else {
    return date.toLocaleDateString('zh-CN')
  }
}

const confirmDelete = (doc: Document) => {
  documentToDelete.value = doc
  showDeleteModal.value = true
}

const deleteDocument = () => {
  if (documentToDelete.value) {
    const index = documents.value.findIndex(d => d.id === documentToDelete.value!.id)
    if (index > -1) {
      documents.value.splice(index, 1)
    }
    showDeleteModal.value = false
    documentToDelete.value = null
  }
}

const downloadDocument = (doc: Document) => {
  // 模拟下载
  alert(`开始下载: ${doc.name}`)
}

// 拖拽上传
const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  isDragging.value = true
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  isDragging.value = false
  const files = e.dataTransfer?.files
  if (files) {
    Array.from(files).forEach(file => uploadFile(file))
  }
}

// 生命周期
onMounted(() => {
  document.addEventListener('dragover', handleDragOver)
  // 组件挂载时自动获取文档列表
  fetchDocuments()
})

onUnmounted(() => {
  document.removeEventListener('dragover', handleDragOver)
})
</script>

<style scoped>
.knowledge-base {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: linear-gradient(135deg, #F5F8FF 0%, #E8EFFF 50%, #F0F6FF 100%);
  position: relative;
}

/* 头部样式 */
.kb-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #D4DDFD;
}

.kb-header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.kb-back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1px solid #D4DDFD;
  background: white;
  cursor: pointer;
  color: #5A7BD6;
  border-radius: 10px;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
  margin-right: 8px;
}

.kb-back-btn:hover {
  background: #F5F8FF;
  border-color: #A6BDFB;
  transform: translateX(-2px);
}

.kb-back-btn svg {
  width: 18px;
  height: 18px;
}

.kb-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(166, 189, 251, 0.35);
}

.kb-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.kb-title-section {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.kb-title {
  font-size: 22px;
  font-weight: 700;
  color: #5A7BD6;
  margin: 0;
}

.kb-subtitle {
  font-size: 13px;
  color: #8A9FD8;
  margin: 0;
}

/* 统计卡片 */
.kb-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.6);
}

.stat-card {
  background: white;
  border-radius: 14px;
  padding: 16px 20px;
  border: 1px solid #D4DDFD;
  box-shadow: 0 2px 8px rgba(166, 189, 251, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(166, 189, 251, 0.2);
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #5A7BD6;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: #8A9FD8;
  font-weight: 500;
}

/* 操作栏 */
.kb-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.6);
  border-bottom: 1px solid #D4DDFD;
}

.search-box {
  flex: 1;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #A6BDFB;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 44px;
  border: 1px solid #D4DDFD;
  border-radius: 12px;
  font-size: 14px;
  color: #5A6B8A;
  background: white;
  transition: all 0.3s ease;
  outline: none;
}

.search-input:focus {
  border-color: #A6BDFB;
  box-shadow: 0 0 0 3px rgba(166, 189, 251, 0.2);
}

.search-input::placeholder {
  color: #A6BDFB;
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(166, 189, 251, 0.35);
}

.upload-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(166, 189, 251, 0.45);
  background: linear-gradient(135deg, #8FA8F5 0%, #7896F0 100%);
}

.upload-btn svg {
  width: 18px;
  height: 18px;
}

/* 内容区域 */
.kb-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: linear-gradient(135deg, #F5F8FF 0%, #E8EFFF 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: #A6BDFB;
}

.empty-state h3 {
  font-size: 18px;
  color: #5A7BD6;
  margin-bottom: 8px;
  font-weight: 600;
}

.empty-state p {
  font-size: 14px;
  color: #8A9FD8;
  max-width: 300px;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid #E8EFFF;
  border-top-color: #A6BDFB;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  font-size: 14px;
  color: #8A9FD8;
}

/* 错误状态 */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.error-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: linear-gradient(135deg, #FFE8E8 0%, #FFF0F0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.error-icon svg {
  width: 40px;
  height: 40px;
  color: #FF6B6B;
}

.error-state h3 {
  font-size: 18px;
  color: #FF6B6B;
  margin-bottom: 8px;
  font-weight: 600;
}

.error-state p {
  font-size: 14px;
  color: #8A9A9A;
  max-width: 300px;
  margin-bottom: 20px;
}

.retry-btn {
  padding: 10px 24px;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(166, 189, 251, 0.35);
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(166, 189, 251, 0.45);
}

/* 文档列表 */
.document-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.document-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: white;
  border-radius: 14px;
  border: 1px solid #D4DDFD;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(166, 189, 251, 0.08);
}

.document-item:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 16px rgba(166, 189, 251, 0.15);
  border-color: #A6BDFB;
}

.document-item.uploading {
  opacity: 0.8;
}

.document-item.error {
  border-color: #FFB4B4;
  background: linear-gradient(135deg, #FFF5F5 0%, #FFFFFF 100%);
}

.doc-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.doc-icon.file-pdf {
  background: linear-gradient(135deg, #FFE8E8 0%, #FFF0F0 100%);
  color: #FF6B6B;
}

.doc-icon.file-word {
  background: linear-gradient(135deg, #E8F0FF 0%, #F0F5FF 100%);
  color: #5A7BD6;
}

.doc-icon.file-text {
  background: linear-gradient(135deg, #E8FFF0 0%, #F0FFF5 100%);
  color: #6BCB77;
}

.doc-icon.file-other {
  background: linear-gradient(135deg, #F5F8FF 0%, #F0F6FF 100%);
  color: #A6BDFB;
}

.doc-icon svg {
  width: 24px;
  height: 24px;
}

.doc-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.doc-name {
  font-size: 15px;
  font-weight: 600;
  color: #5A6B8A;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.doc-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #8A9FD8;
}

.doc-type {
  padding: 2px 8px;
  background: #F5F8FF;
  border-radius: 4px;
  font-weight: 500;
}

.upload-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 4px;
}

.progress-bar {
  flex: 1;
  height: 4px;
  background: #E8EFFF;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #A6BDFB 0%, #8FA8F5 100%);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 11px;
  color: #A6BDFB;
  font-weight: 600;
  min-width: 32px;
  text-align: right;
}

.upload-error {
  font-size: 12px;
  color: #FF6B6B;
  margin-top: 4px;
}

.doc-actions {
  display: flex;
  gap: 8px;
}

.doc-action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: none;
  background: #F5F8FF;
  cursor: pointer;
  color: #5A7BD6;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-size: 13px;
  font-weight: 500;
}

.doc-action-btn:hover:not(:disabled) {
  background: #E8EFFF;
  color: #4A6BC6;
  transform: translateY(-1px);
}

.doc-action-btn.delete {
  background: #FFF0F0;
  color: #FF6B6B;
}

.doc-action-btn.delete:hover:not(:disabled) {
  background: #FFE8E8;
  color: #FF5252;
  transform: translateY(-1px);
}

.doc-action-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.doc-action-btn svg {
  width: 16px;
  height: 16px;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 32px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
}

.modal-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.modal-icon.warning {
  background: linear-gradient(135deg, #FFE8E8 0%, #FFF0F0 100%);
  color: #FF6B6B;
}

.modal-icon svg {
  width: 32px;
  height: 32px;
}

.modal-content h3 {
  font-size: 20px;
  color: #5A6B8A;
  margin-bottom: 12px;
  font-weight: 700;
}

.modal-content p {
  font-size: 14px;
  color: #8A9A9A;
  margin-bottom: 24px;
  line-height: 1.6;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.modal-btn {
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.modal-btn.cancel {
  background: #F5F8FF;
  color: #8A9A9A;
}

.modal-btn.cancel:hover {
  background: #E8EFFF;
  color: #5A7BD6;
}

.modal-btn.confirm {
  background: linear-gradient(135deg, #FF6B6B 0%, #FF5252 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.35);
}

.modal-btn.confirm:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.45);
}

/* 拖拽遮罩 */
.drag-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(166, 189, 251, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  animation: fadeIn 0.2s ease;
}

.drag-content {
  text-align: center;
  color: white;
}

.drag-content svg {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
}

.drag-content p {
  font-size: 20px;
  font-weight: 600;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(20px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

/* 文件上传加载画面 */
.upload-loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(90, 106, 138, 0.75);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.upload-loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  padding: 40px 48px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(90, 106, 138, 0.3);
  animation: slideUp 0.4s ease;
  max-width: 90%;
}

.upload-spinner-container {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-spinner {
  position: absolute;
  width: 80px;
  height: 80px;
  animation: rotate 2s linear infinite;
}

.spinner-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid transparent;
  animation: pulse 1.5s ease-in-out infinite;
}

.spinner-ring:nth-child(1) {
  border-top-color: #A6BDFB;
  animation-delay: 0s;
}

.spinner-ring:nth-child(2) {
  border-right-color: #8FA8F5;
  animation-delay: 0.15s;
}

.spinner-ring:nth-child(3) {
  border-bottom-color: #6B8AF5;
  animation-delay: 0.3s;
}

.upload-icon {
  width: 32px;
  height: 32px;
  color: #5A7BD6;
  animation: bounce 1s ease-in-out infinite;
}

.upload-loading-text {
  text-align: center;
}

.upload-status {
  font-size: 16px;
  font-weight: 600;
  color: #5A6B8A;
  margin: 0 0 8px 0;
}

.upload-filename {
  font-size: 14px;
  color: #8A9FD8;
  margin: 0;
  max-width: 280px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to { 
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { 
    transform: scale(0.9);
    opacity: 0.7;
  }
  50% { 
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

/* 滚动条样式 */
.kb-content::-webkit-scrollbar {
  width: 6px;
}

.kb-content::-webkit-scrollbar-track {
  background: transparent;
}

.kb-content::-webkit-scrollbar-thumb {
  background: rgba(166, 189, 251, 0.5);
  border-radius: 3px;
}

.kb-content::-webkit-scrollbar-thumb:hover {
  background: rgba(166, 189, 251, 0.7);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .kb-stats {
    grid-template-columns: 1fr;
    padding: 16px;
  }
  
  .kb-header {
    padding: 16px;
  }
  
  .kb-back-btn {
    padding: 8px 12px;
    font-size: 13px;
  }
  
  .kb-back-btn span {
    display: none;
  }
  
  .kb-icon {
    width: 40px;
    height: 40px;
  }
  
  .kb-title {
    font-size: 18px;
  }
  
  .kb-actions {
    flex-direction: column;
    padding: 16px;
  }
  
  .search-box {
    width: 100%;
  }
  
  .upload-btn {
    width: 100%;
    justify-content: center;
  }
  
  .kb-content {
    padding: 16px;
  }
  
  .document-item {
    padding: 12px 16px;
    flex-wrap: wrap;
  }
  
  .doc-meta {
    flex-wrap: wrap;
  }
  
  .doc-actions {
    width: 100%;
    justify-content: flex-end;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #E8EFFF;
  }
  
  .doc-action-btn {
    flex: 1;
    justify-content: center;
    max-width: 100px;
  }
}
</style>
