<template>
  <div class="chat-page">
    <!-- 移动端遮罩 -->
    <div v-if="showSidebar && isMobile && currentModule === 'qa'" class="sidebar-overlay" @click="showSidebar = false"></div>
    
    <!-- 左侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed, show: showSidebar, 'sidebar-hidden': currentModule !== 'qa' && isMobile }">
      <div class="sidebar-header">
        <div class="logo" v-if="!sidebarCollapsed">
          <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="20" cy="20" r="18" fill="#99CDD8"/>
            <path d="M20 8L32 20L20 32L8 20L20 8Z" fill="white"/>
          </svg>
          <span>StudySaviorPro</span>
        </div>
      </div>

      <!-- 功能模块 -->
      <div class="function-modules" v-if="!sidebarCollapsed">
        <div class="module-title">功能模块</div>
        <div class="module-list">
          <div class="module-item" :class="{ active: currentModule === 'qa' }" @click="currentModule = 'qa'">
            <div class="module-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
            </div>
            <div class="module-info">
              <div class="module-name">智能问答</div>
              <div class="module-desc">智能回答问题</div>
            </div>
          </div>

          <div class="module-item" :class="{ active: currentModule === 'knowledge' }" @click="currentModule = 'knowledge'">
            <div class="module-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                <path d="M12 6l-4 4h8l-4 4"/>
              </svg>
            </div>
            <div class="module-info">
              <div class="module-name">知识库</div>
              <div class="module-desc">管理和查询知识</div>
            </div>
          </div>

          <div class="module-item" :class="{ active: currentModule === 'quiz' }" @click="currentModule = 'quiz'">
            <div class="module-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10 9 9 9 8 9"/>
              </svg>
            </div>
            <div class="module-info">
              <div class="module-name">智能出题</div>
              <div class="module-desc">自动生成题目</div>
            </div>
          </div>
        </div>
      </div>

      <button class="new-chat-btn" @click="startNewChat" v-if="!sidebarCollapsed">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        <span>新建对话</span>
      </button>

      <div class="chat-history">
        <div class="history-title" v-if="!sidebarCollapsed">最近对话</div>
        <div class="history-list">
          <div 
            v-for="(chat, index) in chatHistory" 
            :key="index"
            class="history-item"
            :class="{ active: currentChatId === chat.id }"
            @click="selectChat(chat.id)"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            <div v-if="!sidebarCollapsed" class="chat-info">
              <span class="chat-title">{{ chat.title }}</span>
              <span class="chat-time">{{ formatDate(chat.created_at) }}</span>
            </div>
            <button 
              v-if="!sidebarCollapsed" 
              class="delete-btn" 
              @click.stop="showDeleteConfirmModal(chat.id)"
              title="删除会话"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div class="sidebar-footer" v-if="!sidebarCollapsed">
        <div class="user-info">
          <div class="avatar">{{ username.charAt(0).toUpperCase() }}</div>
          <span>{{ username }}</span>
        </div>
      </div>
    </aside>

    <!-- 知识库模块 -->
      <main class="knowledge-main" v-if="currentModule === 'knowledge'">
        <header class="chat-header">
          <div class="header-left">
            <div class="model-selector">
              <span>知识库</span>
            </div>
          </div>
          <div class="header-right">
            <button class="header-btn" title="设置">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
            </button>
          </div>
        </header>

        <div class="knowledge-content">
          <!-- 统计卡片 -->
          <div class="stats-cards">
            <div class="stat-card">
              <div class="stat-value">{{ knowledgeDocuments.length }}</div>
              <div class="stat-label">文档总数</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ totalKnowledgeSize }}</div>
              <div class="stat-label">存储空间</div>
            </div>
            <div class="stat-card">
              <div class="stat-value">{{ recentKnowledgeUploads }}</div>
              <div class="stat-label">本周上传</div>
            </div>
          </div>

          <!-- 搜索栏 -->
          <div class="search-bar">
            <div class="search-input-wrapper">
              <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
              </svg>
              <input type="text" class="search-input" placeholder="搜索文档..." />
            </div>
            <button class="refresh-btn" @click="loadKnowledgeDocuments" :disabled="knowledgeLoading" title="刷新列表">
              <svg :class="{ spinning: knowledgeLoading }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="23 4 23 10 17 10"/>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
              </svg>
              <span>刷新</span>
            </button>
            <button class="upload-btn" @click="triggerUpload">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              <span>上传文档</span>
            </button>
            <input 
              type="file" 
              ref="fileInput" 
              style="display: none" 
              accept=".pdf,.txt,.doc,.docx"
              @change="handleFileUpload"
            />
          </div>

          <!-- 文档列表 - 从后端动态加载 -->
          <div class="document-list">
            <div class="loading-state" v-if="knowledgeLoading">
              <div class="loading-spinner"></div>
              <p>正在加载文档...</p>
            </div>
            <div class="empty-state" v-else-if="knowledgeDocuments.length === 0">
              <div class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10 9 9 9 8 9"/>
                </svg>
              </div>
              <h3>暂无文档</h3>
              <p>点击上方"上传文档"按钮添加您的第一个文档</p>
            </div>
            <div 
              v-else
              v-for="doc in knowledgeDocuments" 
              :key="doc.id"
              class="document-item"
            >
              <div class="doc-icon" :class="doc.type">
                <svg v-if="doc.type === 'pdf'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
                <svg v-else-if="doc.type === 'word'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
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
                <div class="doc-type">{{ doc.typeLabel }}</div>
                <div class="doc-size">{{ doc.size }}</div>
                <div class="doc-date">{{ doc.date }}</div>
              </div>
              <div class="doc-name">{{ doc.name }}</div>
              <div class="doc-actions">
                <button class="action-btn download" @click="downloadDoc(doc)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                  <span>下载</span>
                </button>
                <button class="action-btn delete" @click="deleteDoc(doc)">
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

        <!-- 文件上传加载画面 - 非阻塞式，固定在右下角 -->
        <div v-if="isUploading" class="upload-toast" :class="uploadStatus">
          <div class="upload-toast-content">
            <div class="upload-toast-icon">
              <svg v-if="uploadStatus === 'uploading'" class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" stroke-dasharray="60" stroke-dashoffset="20"/>
              </svg>
              <svg v-else-if="uploadStatus === 'success'" class="success-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
              </svg>
              <svg v-else class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="15" y1="9" x2="9" y2="15"/>
                <line x1="9" y1="9" x2="15" y2="15"/>
              </svg>
            </div>
            <div class="upload-toast-info">
              <p class="upload-toast-filename">{{ uploadingFileName }}</p>
              <p class="upload-toast-status">{{ uploadStatusText }}</p>
              <div v-if="uploadStatus === 'uploading'" class="upload-progress-bar">
                <div class="upload-progress-fill" :style="{ width: uploadProgress + '%' }"></div>
              </div>
            </div>
            <button v-if="uploadStatus === 'uploading'" class="upload-cancel-btn" @click="cancelUpload" title="取消上传">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
            <button v-else class="upload-close-btn" @click="closeUploadToast" title="关闭">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        </div>
      </main>

    <!-- 智能出题模块 -->
    <main class="knowledge-main" v-if="currentModule === 'quiz'">
      <header class="chat-header">
        <div class="header-left">
          <div class="model-selector">
            <span>智能出题</span>
          </div>
        </div>
        <div class="header-right">
          <button class="header-btn" title="设置">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
            </svg>
          </button>
        </div>
      </header>

      <!-- 题目类型选择栏 -->
      <div class="quiz-type-bar">
        <div class="type-options">
          <button 
            class="type-option" 
            :class="{ active: selectedQuizType === 'choice' }"
            @click="selectedQuizType = 'choice'"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            <span>选择题</span>
          </button>
          <button 
            class="type-option" 
            :class="{ active: selectedQuizType === 'truefalse' }"
            @click="selectedQuizType = 'truefalse'"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            <span>判断题</span>
          </button>
          <button 
            class="type-option" 
            :class="{ active: selectedQuizType === 'fill' }"
            @click="selectedQuizType = 'fill'"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 19l7-7 3 3-7 7-3-3z"/>
              <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
              <path d="M2 2l7.586 7.586"/>
              <circle cx="11" cy="11" r="2"/>
            </svg>
            <span>填空题</span>
          </button>
          <button 
            class="type-option" 
            :class="{ active: selectedQuizType === 'subjective' }"
            @click="selectedQuizType = 'subjective'"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
            <span>主观题</span>
          </button>
        </div>
        <button class="history-btn" @click="loadHistoryQuestions" :disabled="isLoadingHistory">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <span>历史生成</span>
        </button>
      </div>

      <div class="knowledge-content">
        <!-- 知识点输入框 -->
        <div class="knowledge-input-section">
          <div class="input-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 20h9"/>
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
            </svg>
            <span>请输入知识点</span>
          </div>
          <div class="knowledge-input-wrapper">
            <textarea
              v-model="knowledgePoint"
              placeholder="请输入需要生成题目的知识点，例如：三角函数、牛顿定律、Python 基础语法..."
              rows="3"
              class="knowledge-input"
            ></textarea>
            <div class="generate-controls">
              <button class="generate-btn" @click="generateQuiz" :disabled="!knowledgePoint.trim() || isGenerating">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                </svg>
                <span>{{ isGenerating ? '生成中...' : '生成题目' }}</span>
              </button>
              <div class="quiz-count-input">
                <label class="count-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="label-icon">
                    <line x1="8" y1="6" x2="21" y2="6"/>
                    <line x1="8" y1="12" x2="21" y2="12"/>
                    <line x1="8" y1="18" x2="21" y2="18"/>
                    <line x1="3" y1="6" x2="3.01" y2="6"/>
                    <line x1="3" y1="12" x2="3.01" y2="12"/>
                    <line x1="3" y1="18" x2="3.01" y2="18"/>
                  </svg>
                  <span>题目数量</span>
                </label>
                <div class="count-input-wrapper">
                  <button class="count-btn" @click="decreaseCount" :disabled="quizCount <= 1">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <line x1="5" y1="12" x2="19" y2="12"/>
                    </svg>
                  </button>
                  <input
                    type="number"
                    v-model="quizCount"
                    :min="1"
                    :max="20"
                    class="count-input"
                    placeholder="1"
                  />
                  <button class="count-btn" @click="increaseCount" :disabled="quizCount >= 20">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <line x1="12" y1="5" x2="12" y2="19"/>
                      <line x1="5" y1="12" x2="19" y2="12"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 题目显示区域 -->
        <div v-if="generatedQuestions.length > 0" class="questions-display-section">
          <div class="questions-header">
            <h2>生成的题目</h2>
            <button class="export-btn" title="导出题目">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              <span>导出</span>
            </button>
          </div>
          
          <div class="questions-list">
            <div 
              v-for="(item, index) in generatedQuestions" 
              :key="index"
              class="question-card"
            >
              <div class="question-header">
                <span class="question-number">第{{ index + 1 }}题</span>
                <span class="question-type-badge" :class="getQuestionTypeClass(item.type)">
                  {{ getQuestionTypeLabel(item.type) }}
                </span>
              </div>
              
              <div class="question-content">
                <div class="question-text">{{ item.question }}</div>
                
                <!-- 选择题选项 -->
                <div v-if="item.type === 0 && item.options" class="question-options">
                  <div 
                    v-for="(option, key) in item.options" 
                    :key="key"
                    class="option-item"
                    :class="getOptionClass(item, String(key))"
                    @click="selectOption(item, String(key))"
                  >
                    <span class="option-label">{{ key }}.</span>
                    <span class="option-content">{{ option }}</span>
                    <span v-if="item.selectedOption === key" class="option-status">
                      <svg v-if="isCorrectAnswer(item, String(key))" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                        <polyline points="20 6 9 17 4 12"/>
                      </svg>
                      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                      </svg>
                    </span>
                  </div>
                </div>
                
                <!-- 判断题按钮 -->
                <div v-if="item.type === 2" class="true-false-buttons">
                  <button 
                    class="tf-btn tf-true"
                    :class="getTrueFalseClass(item, true)"
                    @click="selectTrueFalse(item, true)"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                    <span>正确</span>
                  </button>
                  <button 
                    class="tf-btn tf-false"
                    :class="getTrueFalseClass(item, false)"
                    @click="selectTrueFalse(item, false)"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <line x1="18" y1="6" x2="6" y2="18"/>
                      <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                    <span>错误</span>
                  </button>
                </div>
                
                <!-- 填空题输入框 -->
                <div v-if="item.type === 1" class="fill-input-section">
                  <div class="fill-input-wrapper">
                    <input
                      type="text"
                      v-model="item.userAnswer"
                      :disabled="item.submitted"
                      :class="['fill-input', getFillInputClass(item)]"
                      placeholder="请输入答案"
                      @keyup.enter="submitFillAnswer(item)"
                    />
                    <button
                      v-if="!item.submitted"
                      class="submit-btn"
                      @click="submitFillAnswer(item)"
                      :disabled="!item.userAnswer || !item.userAnswer.trim()"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="20 6 9 17 4 12"/>
                      </svg>
                      <span>提交</span>
                    </button>
                    <span v-else class="submit-status" :class="getFillInputClass(item)">
                      <svg v-if="item.isCorrect" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                        <polyline points="20 6 9 17 4 12"/>
                      </svg>
                      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                      </svg>
                    </span>
                  </div>
                </div>
              </div>
              
              <div class="question-footer">
                <button 
                  class="show-answer-btn" 
                  @click="item.showAnswer = !item.showAnswer"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  <span>{{ item.showAnswer ? '隐藏答案' : '查看答案' }}</span>
                </button>
                
                <div v-show="item.showAnswer" class="answer-section">
                  <div class="answer-item">
                    <span class="answer-label">正确答案:</span>
                    <span class="answer-value">{{ formatAnswer(item.answer, item.type) }}</span>
                  </div>
                  <div class="answer-item">
                    <span class="answer-label">解析:</span>
                    <div class="answer-explanation">{{ item.explanation }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 历史记录面板 -->
        <div v-if="showHistoryPanel" class="history-panel">
          <div class="history-header">
            <h3>历史生成记录</h3>
            <button class="close-btn" @click="showHistoryPanel = false">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          <div class="history-list">
            <div 
              v-for="(history, index) in historyList" 
              :key="history.id || index"
              class="history-item"
              @click="loadHistoryQuestion(history)"
            >
              <div class="history-info">
                <div class="history-title">{{ history.original_question }}</div>
                <div class="history-meta">
                  <span class="history-type">{{ getQuestionTypeLabel(history.question_type) }}</span>
                  <span class="history-date">{{ formatDate(history.created_at) }}</span>
                </div>
              </div>
              <svg class="history-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 18 15 12 9 6"/>
              </svg>
            </div>
            <div v-if="historyList.length === 0" class="history-empty">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              <p>暂无历史记录</p>
            </div>
          </div>
        </div>

        <!-- 历史题目详情弹窗 -->
        <transition name="modal">
          <div v-if="showHistoryDetail" class="history-detail-overlay" @click.self="closeHistoryDetail">
            <div class="history-detail-modal">
              <div class="detail-header">
                <h3>
                  <span class="detail-type-badge" :class="getQuestionTypeClass(currentHistoryDetail?.question_type)">
                    {{ getQuestionTypeLabel(currentHistoryDetail?.question_type) }}
                  </span>
                  <span class="detail-title">{{ currentHistoryDetail?.original_question }}</span>
                </h3>
                <button class="close-btn" @click="closeHistoryDetail">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
              <div class="detail-content">
                <div 
                  v-for="(item, index) in currentHistoryDetail?.questions" 
                  :key="index"
                  class="detail-question-card"
                >
                  <div class="detail-question-header">
                    <span class="question-number">第{{ index + 1 }}题</span>
                  </div>
                  <div class="detail-question-text">{{ item.question }}</div>
                  
                  <!-- 选择题选项 -->
                  <div v-if="item.options" class="detail-options">
                    <div 
                      v-for="(option, key) in item.options" 
                      :key="key"
                      class="detail-option-item"
                    >
                      <span class="option-label">{{ key }}.</span>
                      <span class="option-content">{{ option }}</span>
                    </div>
                  </div>
                  
                  <!-- 答案和解析 -->
                  <div class="detail-answer-section">
                    <div class="answer-label">正确答案:</div>
                    <div class="answer-value">{{ formatAnswer(item.answer, currentHistoryDetail?.question_type) }}</div>
                    <div class="answer-label" style="margin-top: 12px;">解析:</div>
                    <div class="detail-explanation">{{ item.explanation }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </transition>

      </div>
    </main>

    <!-- 主聊天区域 -->
    <main class="chat-main" v-if="currentModule === 'qa'">
      <!-- 顶部导航 -->
      <header class="chat-header">
        <div class="header-left">
        </div>
        <div class="header-right">
          <template v-if="isBatchDeleteMode">
            <button class="header-btn batch-delete-btn" @click="batchDeleteMessages" title="删除选中消息">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
              <span class="batch-delete-count" v-if="selectedMessages.length > 0">{{ selectedMessages.length }}</span>
            </button>
            <button class="header-btn cancel-batch-btn" @click="toggleBatchDeleteMode" title="取消">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </template>
          <button v-else class="header-btn" @click="toggleBatchDeleteMode" title="批量删除">
            <svg viewBox="0 0 24 24" fill="none" class="batch-delete-icon">
              <rect x="3" y="3" width="18" height="18" rx="5" ry="5" class="rect-bg"/>
              <line x1="9" y1="9" x2="15" y2="15" class="x-line"/>
              <line x1="15" y1="9" x2="9" y2="15" class="x-line"/>
            </svg>
          </button>
        </div>
      </header>

      <!-- 聊天内容区域 -->
      <div class="chat-content" ref="messagesContainer" @scroll="handleScroll">
        <div v-if="messages.length === 0" class="welcome-message">
          <h1>你好，我是 AI 助手</h1>
          <p>有什么可以帮助你的吗？</p>
        </div>

        <div class="messages-container">
          <div 
            v-for="(message, index) in messages" 
            :key="index"
            class="message"
            :class="[message.role, { selected: selectedMessages.includes(message.id!) }]"
          >
            <div class="message-checkbox" 
                 v-if="isBatchDeleteMode && message.id" 
                 @click.stop="toggleMessageSelection(message.id)"
                 :class="{ checked: selectedMessages.includes(message.id) }">
              <svg v-if="selectedMessages.includes(message.id)" viewBox="0 0 24 24" fill="currentColor">
                <rect x="3" y="3" width="18" height="18" rx="2" fill="#6366F1"/>
                <path d="M9 12l2 2 4-4" stroke="white" stroke-width="2" fill="none"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
              </svg>
            </div>
            <div class="message-avatar" v-if="message.role === 'assistant'">
              <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="20" cy="20" r="18" fill="#99CDD8"/>
                <path d="M20 8L32 20L20 32L8 20L20 8Z" fill="white"/>
              </svg>
            </div>
            <div class="message-content">
              <div class="message-header">
                <span class="message-name">{{ message.role === 'user' ? username : 'AI 助手' }}</span>
                <span class="message-time">{{ message.time }}</span>
                <!-- 等待动画 - 只在最后一条AI消息且发送中时显示 -->
                <span v-if="isSending && message.role === 'assistant' && index === messages.length - 1" class="thinking-inline">
                  <span class="thinking-text-small">正在拼命思考中</span>
                  <span class="thinking-dots-inline">
                    <span></span>
                    <span></span>
                    <span></span>
                  </span>
                </span>
              </div>
              <div class="message-text" v-html="message.role === 'assistant' ? renderMarkdown(message.content) : filterContent(message.content)"></div>
              <div class="message-actions" v-if="message.role === 'assistant'">
                <button class="action-btn" title="复制">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                  </svg>
                </button>
                <button class="action-btn" title="重新生成">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="23 4 23 10 17 10"/>
                    <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                  </svg>
                </button>
                <button class="action-btn" title="点赞">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/>
                  </svg>
                </button>
                <button class="action-btn" title="点踩">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"/>
                  </svg>
                </button>
                <button class="action-btn delete-message-btn" title="删除此消息" @click="deleteSingleMessage(index)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <div class="input-container">
          <textarea
            v-model="inputMessage"
            @keydown.enter.exact.prevent="sendMessage"
            placeholder="输入消息..."
            rows="1"
            ref="inputRef"
          ></textarea>
          <div class="input-actions">
            <div class="action-buttons">
              <button class="input-btn" title="上传文件">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
                </svg>
              </button>
              <button class="input-btn" title="搜索">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"/>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                </svg>
              </button>
            </div>
            <button class="send-btn" @click="sendMessage" :disabled="!inputMessage.trim() || isSending">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="22" y1="2" x2="11" y2="13"/>
                <polygon points="22 2 15 22 11 13 2 9 22 2"/>
              </svg>
            </button>
          </div>
        </div>
        <p class="input-hint">AI 生成的内容可能不准确，请仔细甄别</p>
      </div>
    </main>
    
    <!-- 自定义提示框 -->
    <transition name="toast">
      <div v-if="showToast" class="toast" :class="toastType">
        <div class="toast-icon">
          <svg v-if="toastType === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
        </div>
        <span class="toast-message">{{ toastMessage }}</span>
      </div>
    </transition>

    <!-- 认证错误弹窗 -->
    <transition name="modal">
      <div v-if="showAuthError" class="modal-overlay" @click.self="goToLogin">
        <div class="modal-container">
          <div class="modal-header">
            <svg class="modal-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <h3>认证失败</h3>
          </div>
          <div class="modal-body">
            <p>{{ authErrorMessage }}</p>
            <p class="modal-hint">您需要重新登录才能继续使用</p>
          </div>
          <div class="modal-footer">
            <button class="modal-btn primary" @click="goToLogin">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <polyline points="16 17 21 12 16 7"/>
                <line x1="21" y1="12" x2="9" y2="12"/>
              </svg>
              <span>返回登录</span>
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- 删除确认弹窗 -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click.self="cancelDelete">
      <div class="modal-content">
        <div class="modal-icon warning">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        </div>
        <h3>确认删除</h3>
        <p>确定要删除这个会话吗？删除后无法恢复。</p>
        <div class="modal-actions">
          <button class="modal-btn cancel" @click="cancelDelete">取消</button>
          <button class="modal-btn confirm" @click="confirmDeleteChatSession">确认删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick, onMounted, onUnmounted, computed, triggerRef } from 'vue'
import { useRouter } from 'vue-router'
import MarkdownIt from 'markdown-it'

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true
})

const router = useRouter()
const sidebarCollapsed = ref(false)
const showSidebar = ref(false)
const isMobile = ref(false)
const username = ref('Admin')
const inputMessage = ref('')
const isSending = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const inputRef = ref<HTMLTextAreaElement | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const selectedQuizType = ref('choice') // 默认选中选择题
const knowledgePoint = ref('') // 知识点输入
const quizCount = ref(1) // 题目数量，默认 1 道
const isGenerating = ref(false) // 生成中状态
const generatedQuestions = ref<Array<any>>([]) // 生成的题目列表
const showHistoryPanel = ref(false) // 显示历史面板
const historyList = ref<Array<any>>([]) // 历史记录列表
const isLoadingHistory = ref(false) // 加载中状态
const showHistoryDetail = ref(false) // 显示历史题目详情
const currentHistoryDetail = ref<any>(null) // 当前查看的历史题目详情

// 减少题目数量
const decreaseCount = () => {
  if (quizCount.value > 1) {
    quizCount.value = Math.max(1, quizCount.value - 1)
  }
}

// 增加题目数量
const increaseCount = () => {
  if (quizCount.value < 20) {
    quizCount.value = Math.min(20, quizCount.value + 1)
  }
}

// 获取题型对应的数字
const getQuestionTypeNumber = (): number => {
  const typeMap: Record<string, number> = {
    'choice': 0,      // 选择题
    'fill': 1,        // 填空题
    'truefalse': 2,   // 判断题
    'subjective': 3   // 主观题
  }
  return typeMap[selectedQuizType.value] || 0
}

// 获取题型标签
const getQuestionTypeLabel = (type: number): string => {
  const labels: Record<number, string> = {
    0: '选择题',
    1: '填空题',
    2: '判断题',
    3: '主观题'
  }
  return labels[type] || '未知题型'
}

// 获取题型样式类
const getQuestionTypeClass = (type: number): string => {
  const classes: Record<number, string> = {
    0: 'type-choice',
    1: 'type-fill',
    2: 'type-truefalse',
    3: 'type-subjective'
  }
  return classes[type] || ''
}

// 格式化答案显示
const formatAnswer = (answer: any, type: number): string => {
  if (type === 0) { // 选择题
    return Array.isArray(answer) ? answer.join(', ') : answer
  } else if (type === 2) { // 判断题
    return answer === 1 ? '正确' : '错误'
  }
  return String(answer)
}

// 解析后端返回的题目数据
const parseQuestionsFromResponse = (responseData: any, questionType: number) => {
  if (!responseData || !responseData.questions || !Array.isArray(responseData.questions)) {
    console.error('题目数据格式错误:', responseData)
    return []
  }
  
  return responseData.questions.map((q: any, index: number) => ({
    type: questionType,
    question: q.question || '',
    options: q.options || null, // 选择题选项
    answer: q.answer,
    explanation: q.explanation || '',
    showAnswer: false, // 默认不显示答案
    selectedOption: null, // 用户选择的选项 (选择题/判断题)
    userAnswer: '', // 填空题用户输入的答案
    submitted: false, // 是否已提交
    isCorrect: false // 答案是否正确
  }))
}

// 选择题：选择选项
const selectOption = (item: any, optionKey: string) => {
  if (item.type !== 0) return // 只处理选择题
  item.selectedOption = optionKey
}

// 判断题：选择正确/错误
const selectTrueFalse = (item: any, isTrue: boolean) => {
  if (item.type !== 2) return // 只处理判断题
  item.selectedOption = isTrue ? 1 : 0 // 1 表示正确，0 表示错误
}

// 判断是否是正确答案
const isCorrectAnswer = (item: any, optionKey: string): boolean => {
  if (item.type !== 0) return false
  const correctAnswer = item.answer
  // 答案可能是字符串 "A" 或数组 ["A", "B"] (多选题)
  if (Array.isArray(correctAnswer)) {
    return correctAnswer.includes(optionKey)
  }
  return correctAnswer === optionKey
}

// 判断题：判断是否正确
const isTrueFalseCorrect = (item: any, userChoice: boolean): boolean => {
  if (item.type !== 2) return false
  const correctAnswer = item.answer // 1 表示正确，0 表示错误
  const userValue = userChoice ? 1 : 0
  return correctAnswer === userValue
}

// 填空题：提交答案
const submitFillAnswer = (item: any) => {
  if (item.type !== 1 || !item.userAnswer) return
  item.submitted = true
  // 对比答案 (支持多个正确答案，用数组或字符串表示)
  const userAnswer = item.userAnswer.trim()
  const correctAnswer = item.answer
  
  if (Array.isArray(correctAnswer)) {
    // 答案可能是数组 ["答案 1", "答案 2"]
    item.isCorrect = correctAnswer.some(ans => ans.trim() === userAnswer)
  } else {
    // 答案是字符串
    item.isCorrect = correctAnswer.trim() === userAnswer
  }
}

// 获取填空题输入框样式类
const getFillInputClass = (item: any): string => {
  if (item.type !== 1 || !item.submitted) return ''
  return item.isCorrect ? 'fill-correct' : 'fill-wrong'
}

// 获取判断题按钮样式类
const getTrueFalseClass = (item: any, isTrue: boolean): string => {
  if (item.type !== 2 || item.selectedOption === undefined) return ''
  
  const userChoice = isTrue ? 1 : 0
  const isSelected = item.selectedOption === userChoice
  const isCorrect = isTrueFalseCorrect(item, isTrue)
  
  if (isSelected) {
    return isCorrect ? 'tf-correct' : 'tf-wrong'
  }
  return ''
}

// 获取选项样式类
const getOptionClass = (item: any, optionKey: string): string => {
  if (item.type !== 0 || item.selectedOption === undefined) return ''
  
  const isSelected = item.selectedOption === optionKey
  const isCorrect = isCorrectAnswer(item, optionKey)
  
  if (isSelected) {
    return isCorrect ? 'option-correct' : 'option-wrong'
  }
  return ''
}

const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref<'success' | 'error'>('success')
const showAuthError = ref(false) // 认证错误弹窗
const authErrorMessage = ref('') // 认证错误消息
const isUserScrolling = ref(false) // 用户是否正在手动滚动
let scrollTimeout: ReturnType<typeof setTimeout> | null = null // 滚动状态检测防抖定时器

// 删除确认弹窗
const showDeleteConfirm = ref(false)
const sessionToDelete = ref<number | null>(null)

// 获取会话列表
const loadChatSessions = async () => {
  try {
    const token = getToken()
    console.log('开始加载会话列表，token:', token ? '存在' : '不存在')
    const response = await fetch('/agent/question/get_chat_sessions', {
      method: 'GET',
      headers: {
        'Authorization': token || ''
      }
    })
    
    const result = await response.json()
    console.log('会话列表响应:', result)
    
    if (result.code === 1 && result.data && Array.isArray(result.data)) {
      chatHistory.value = result.data.map((session: any) => ({
        id: session.id,
        title: session.title,
        created_at: session.created_at
      }))
      console.log('会话列表已更新:', chatHistory.value)
    } else {
      console.warn('会话列表数据格式不正确:', result)
    }
  } catch (error) {
    console.error('获取会话列表失败:', error)
  }
}

// 显示删除确认弹窗
const showDeleteConfirmModal = (sessionId: number) => {
  sessionToDelete.value = sessionId
  showDeleteConfirm.value = true
}

// 取消删除
const cancelDelete = () => {
  showDeleteConfirm.value = false
  sessionToDelete.value = null
}

// 确认删除会话
const confirmDeleteChatSession = async () => {
  if (!sessionToDelete.value) return
  
  const sessionId = sessionToDelete.value
  showDeleteConfirm.value = false
  sessionToDelete.value = null
  
  try {
    const token = getToken()
    const response = await fetch(`/agent/question/delete_chat_session/${sessionId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': token || ''
      }
    })
    
    const result = await response.json()
    console.log('删除会话响应:', result)
    
    if (response.status === 401 || (result.code === 0 && result.message === 'Not authenticated')) {
      checkAuthError(result)
      return
    }
    
    if (result.code === 1) {
      showMessage('会话已成功删除', 'success')
      // 从列表中移除已删除的会话
      chatHistory.value = chatHistory.value.filter(chat => chat.id !== sessionId)
      // 如果删除的是当前会话，清空当前会话
      if (currentChatId.value === sessionId) {
        currentChatId.value = null
        messages.value = [
          {
            role: 'assistant',
            content: '你好！我是你的 AI 助手，有什么我可以帮助你的吗？',
            time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
          }
        ]
      }
    } else {
      showMessage(result.message || '删除失败', 'error')
    }
  } catch (error) {
    console.error('删除会话失败:', error)
    showMessage('删除会话失败', 'error')
  }
}

const toggleBatchDeleteMode = () => {
  isBatchDeleteMode.value = !isBatchDeleteMode.value
  if (!isBatchDeleteMode.value) {
    selectedMessages.value = []
  }
}

const toggleMessageSelection = (messageId: number) => {
  const index = selectedMessages.value.indexOf(messageId)
  if (index === -1) {
    selectedMessages.value.push(messageId)
  } else {
    selectedMessages.value.splice(index, 1)
  }
}

const batchDeleteMessages = async () => {
  if (selectedMessages.value.length === 0) {
    showMessage('请选择要删除的消息', 'warning')
    return
  }
  
  try {
    const token = getToken()
    const response = await fetch('/agent/question/delete_chat_history', {
      method: 'POST',
      headers: {
        'Authorization': token || '',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(selectedMessages.value)
    })
    
    const result = await response.json()
    console.log('批量删除响应:', result)
    
    if (response.status === 401 || (result.code === 0 && result.message === 'Not authenticated')) {
      checkAuthError(result)
      return
    }
    
    if (result.code === 1) {
      showMessage('消息删除成功', 'success')
      // 从消息列表中移除已删除的消息
      messages.value = messages.value.filter(msg => !selectedMessages.value.includes(msg.id!))
      selectedMessages.value = []
      isBatchDeleteMode.value = false
    } else {
      showMessage(result.message || '删除失败', 'error')
    }
  } catch (error) {
    console.error('批量删除消息失败:', error)
    showMessage('删除消息失败', 'error')
  }
}

const deleteSingleMessage = async (messageIndex: number) => {
  const message = messages.value[messageIndex]
  if (!message || !message.id) {
    showMessage('消息 ID 不存在', 'error')
    return
  }
  
  try {
    const token = getToken()
    const response = await fetch('/agent/question/delete_chat_history', {
      method: 'POST',
      headers: {
        'Authorization': token || '',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify([message.id])
    })
    
    const result = await response.json()
    console.log('删除单条消息响应:', result)
    
    if (response.status === 401 || (result.code === 0 && result.message === 'Not authenticated')) {
      checkAuthError(result)
      return
    }
    
    if (result.code === 1) {
      showMessage('消息删除成功', 'success')
      // 从消息列表中移除已删除的消息
      messages.value.splice(messageIndex, 1)
    } else {
      showMessage(result.message || '删除失败', 'error')
    }
  } catch (error) {
    console.error('删除单条消息失败:', error)
    showMessage('删除消息失败', 'error')
  }
}

// 获取会话历史
const loadChatHistory = async (sessionId: number) => {
  try {
    const token = getToken()
    const response = await fetch(`/agent/question/get_chat_history/${sessionId}`, {
      method: 'GET',
      headers: {
        'Authorization': token || ''
      }
    })
    
    const result = await response.json()
    console.log('会话历史响应:', result)
    
    if (result.code === 1 && result.data && Array.isArray(result.data)) {
      messages.value = result.data.map((chat: any) => ({
        id: chat.id,
        role: chat.role === 0 ? 'user' : 'assistant',
        content: chat.content,
        time: new Date(chat.created_at).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      }))
    }
  } catch (error) {
    console.error('获取会话历史失败:', error)
  }
}

// 滚动到底部函数
const scrollToBottom = (smooth = false, retries = 5, delay = 100) => {
  const attemptScroll = (attempt: number) => {
    if (!messagesContainer.value) return
    
    const container = messagesContainer.value
    const targetScrollTop = container.scrollHeight - container.clientHeight
    
    // 确保滚动到最底部
    if (smooth) {
      container.scrollTo({
        top: targetScrollTop,
        behavior: 'smooth'
      })
    } else {
      container.scrollTop = targetScrollTop
    }
    
    // 继续重试以确保内容完全加载后仍然在底部
    if (attempt < retries) {
      setTimeout(() => {
        attemptScroll(attempt + 1)
      }, delay)
    }
  }
  
  attemptScroll(0)
}

// 用户滚动事件处理
const handleScroll = () => {
  if (!messagesContainer.value) return
  
  const container = messagesContainer.value
  const isAtBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100
  
  if (!isAtBottom) {
    isUserScrolling.value = true
    if (scrollTimeout) {
      clearTimeout(scrollTimeout)
    }
    scrollTimeout = setTimeout(() => {
      isUserScrolling.value = false
    }, 1000)
  } else {
    isUserScrolling.value = false
    if (scrollTimeout) {
      clearTimeout(scrollTimeout)
      scrollTimeout = null
    }
  }
}

// 知识库相关数据
const knowledgeLoading = ref(false)
const isUploading = ref(false)
const uploadingFileName = ref('')
const uploadProgress = ref(0)
const uploadStatus = ref<'uploading' | 'success' | 'error'>('uploading')
const uploadAbortController = ref<AbortController | null>(null)
const uploadStartTime = ref<number>(0)
const uploadLongTimeWarning = ref(false)
const knowledgeDocuments = ref<Array<{
  id: string
  file_id: string
  name: string
  type: string
  typeLabel: string
  size: string
  date: string
  file_size?: number
  created_at?: string
}>>([])

// 知识库统计计算属性
const totalKnowledgeSize = computed(() => {
  // 数据库返回的是 MB，直接累加
  let totalMB = 0
  knowledgeDocuments.value.forEach(doc => {
    // 从原始数据累加（file_size 是 MB 数值）
    if (doc.file_size) {
      totalMB += doc.file_size
    } else {
      // 从 size 字符串解析 MB 值
      const sizeMatch = doc.size.match(/([\d.]+)\s*MB/i)
      if (sizeMatch) {
        totalMB += parseFloat(sizeMatch[1])
      }
    }
  })
  // 转换为合适的单位显示
  if (totalMB >= 1024) {
    return (totalMB / 1024).toFixed(2) + ' GB'
  }
  return totalMB.toFixed(2) + ' MB'
})

const recentKnowledgeUploads = computed(() => {
  const oneWeekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
  return knowledgeDocuments.value.filter(doc => {
    // 从日期字符串解析
    if (doc.created_at) {
      return new Date(doc.created_at) > oneWeekAgo
    }
    // 从显示日期解析
    if (doc.date.includes('天前')) {
      const days = parseInt(doc.date)
      return days < 7
    }
    return false
  }).length
})

// 获取 Token
const getToken = () => {
  return localStorage.getItem('token')
}

// 显示提示框
const showMessage = (message: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

// 检查认证错误并处理
const checkAuthError = (result: any): boolean => {
  console.log('checkAuthError 被调用，result:', result)
  
  // 检查 code=0 的情况 (无论 message 是什么)
  if (result.code === 0) {
    authErrorMessage.value = result.message || '认证失败，请重新登录'
    showAuthError.value = true
    console.log('检测到认证错误 (code=0), 弹出提示框')
    console.log('设置后 showAuthError:', showAuthError.value)
    console.log('设置后 authErrorMessage:', authErrorMessage.value)
    return true
  }
  
  // 检查 message 中包含认证相关关键词的情况
  if (result.message && (
    result.message.toLowerCase().includes('not authenticated') ||
    result.message.toLowerCase().includes('unauthorized') ||
    result.message.toLowerCase().includes('token') ||
    result.message.includes('认证') ||
    result.message.includes('验证')
  )) {
    authErrorMessage.value = result.message
    showAuthError.value = true
    console.log('检测到认证错误 (message 包含关键词), 弹出提示框')
    return true
  }
  
  return false
}

// 返回登录页面
const goToLogin = () => {
  console.log('=== 开始执行 goToLogin ===')
  console.log('当前路由:', router.currentRoute.value.path)
  console.log('准备清除 token')
  
  // 清除本地 Token
  localStorage.removeItem('token')
  console.log('token 已清除，当前 localStorage.token:', localStorage.getItem('token'))
  
  // 确保在下一个 tick 执行路由跳转
  nextTick(() => {
    console.log('准备跳转到根路径 /')
    router.push('/').then(() => {
      console.log('路由跳转成功，当前路由:', router.currentRoute.value.path)
    }).catch((error) => {
      console.error('路由跳转失败:', error)
      // 如果路由跳转失败，尝试使用 window.location
      console.log('尝试使用 window.location.href 跳转')
      window.location.href = '/'
    })
  })
}

// 触发文件上传
const triggerUpload = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

// 上传状态文本计算属性
const uploadStatusText = computed(() => {
  switch (uploadStatus.value) {
    case 'uploading':
      if (uploadLongTimeWarning.value) {
        return '传输需较长时间，请耐心等待'
      }
      return `上传中 ${uploadProgress.value}%`
    case 'success':
      return '上传成功'
    case 'error':
      return '上传失败'
    default:
      return ''
  }
})

// 取消上传
const cancelUpload = () => {
  if (uploadAbortController.value) {
    uploadAbortController.value.abort()
    uploadAbortController.value = null
  }
  uploadStatus.value = 'error'
  uploadProgress.value = 0
  showMessage('上传已取消', 'info')
  setTimeout(() => {
    closeUploadToast()
  }, 2000)
}

// 关闭上传提示
const closeUploadToast = () => {
  isUploading.value = false
  uploadingFileName.value = ''
  uploadProgress.value = 0
  uploadStatus.value = 'uploading'
  uploadAbortController.value = null
  uploadLongTimeWarning.value = false
  uploadStartTime.value = 0
}

// 处理文件上传
const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file) return
  
  isUploading.value = true
  uploadingFileName.value = file.name
  uploadStatus.value = 'uploading'
  uploadProgress.value = 0
  uploadStartTime.value = Date.now()
  uploadLongTimeWarning.value = false
  
  // 创建 AbortController 用于取消上传
  uploadAbortController.value = new AbortController()
  
  // 30秒后显示长时间等待提示
  const longTimeWarningTimeout = setTimeout(() => {
    if (uploadStatus.value === 'uploading') {
      uploadLongTimeWarning.value = true
    }
  }, 30000)
  
  // 验证文件类型
  const allowedTypes = ['.pdf', '.txt', '.doc', '.docx']
  const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
  
  if (!allowedTypes.includes(fileExtension)) {
    uploadStatus.value = 'error'
    showMessage('不支持的文件格式！请上传 PDF、TXT、DOC 或 DOCX 格式的文件。', 'error')
    setTimeout(() => closeUploadToast(), 3000)
    if (target) target.value = ''
    return
  }
  
  // 验证文件大小（限制 100MB）
  const maxSize = 100 * 1024 * 1024
  if (file.size > maxSize) {
    uploadStatus.value = 'error'
    showMessage('文件大小不能超过 100MB！', 'error')
    setTimeout(() => closeUploadToast(), 3000)
    if (target) target.value = ''
    return
  }
  
  // 模拟进度更新
  const progressInterval = setInterval(() => {
    if (uploadProgress.value < 90 && uploadStatus.value === 'uploading') {
      uploadProgress.value += Math.floor(Math.random() * 15) + 5
      if (uploadProgress.value > 90) uploadProgress.value = 90
    }
  }, 300)
  
  try {
    // 创建 FormData 对象
    const formData = new FormData()
    formData.append('file', file)
    
    // 发送 POST 请求到后端（使用相对路径通过 Vite 代理）
    const token = getToken()
    const response = await fetch('/vector/add_documents', {
      method: 'POST',
      headers: {
        'Authorization': token || ''
      },
      body: formData,
      signal: uploadAbortController.value.signal
    })
    
    clearInterval(progressInterval)
    clearTimeout(longTimeWarningTimeout)
    
    console.log('响应状态:', response.status)
    console.log('响应 OK:', response.ok)
    
    // 先读取响应内容
    const result = await response.json()
    console.log('上传结果:', result)
    console.log('返回的 code:', result.code)
    console.log('返回的 message:', result.message)
    
    // 检查认证错误 (包括 401 状态码和 code=0 的情况)
    if (response.status === 401 || (result.code === 0 && result.message === 'Not authenticated')) {
      uploadStatus.value = 'error'
      checkAuthError(result)
      setTimeout(() => closeUploadToast(), 3000)
      return
    }
    
    // 根据返回的 code 判断是否成功
    if (result.code === 1) {
      uploadProgress.value = 100
      uploadStatus.value = 'success'
      showMessage(result.message || `文件 "${file.name}" 上传成功！`, 'success')
      // 上传成功后刷新文档列表
      await loadKnowledgeDocuments()
      // 2秒后自动关闭成功提示
      setTimeout(() => closeUploadToast(), 2000)
    } else {
      uploadStatus.value = 'error'
      showMessage(result.message || '上传失败：未知错误', 'error')
    }

  } catch (error) {
    clearInterval(progressInterval)
    clearTimeout(longTimeWarningTimeout)
    
    if (error instanceof Error && error.name === 'AbortError') {
      console.log('上传被取消')
      return
    }
    
    console.error('上传失败:', error)
    console.error('错误详情:', JSON.stringify(error))
    uploadStatus.value = 'error'
    showMessage('文件上传失败，请稍后重试', 'error')
  } finally {
    uploadAbortController.value = null
    // 重置 input
    if (target) {
      target.value = ''
    }
  }
}

// 加载知识库文档列表
const loadKnowledgeDocuments = async () => {
  knowledgeLoading.value = true
  try {
    const token = getToken()
    const response = await fetch('/vector/get_all_files', {
      headers: {
        'Authorization': token || ''
      }
    })
    
    console.log('HTTP 状态码:', response.status)
    
    // 检查是否是 401 状态码
    if (response.status === 401) {
      // 尝试读取响应内容
      try {
        const errorResult = await response.json()
        console.log('401 错误响应:', errorResult)
        checkAuthError(errorResult)
      } catch (parseError) {
        // 如果无法解析 JSON，使用默认消息
        console.error('解析 401 响应失败:', parseError)
        authErrorMessage.value = '认证失败，请重新登录'
        showAuthError.value = true
      }
      knowledgeDocuments.value = []
      knowledgeLoading.value = false
      return
    }
    
    // 读取响应内容
    const result = await response.json()
    console.log('文档列表响应:', result)
    
    // 检查认证错误 (code=0 的情况)
    if (result.code === 0 && result.message === 'Not authenticated') {
      checkAuthError(result)
      knowledgeDocuments.value = []
      knowledgeLoading.value = false
      return
    }
    
    if (result.code === 1 && Array.isArray(result.data)) {
      // 将后端数据转换为前端格式
      knowledgeDocuments.value = result.data.map((file: any, index: number) => ({
        id: `doc_${index}_${Date.now()}`,
        file_id: file.file_id || file.id || '',
        name: file.original_name,
        type: getFileType(file.original_name),
        typeLabel: getFileTypeLabel(file.original_name),
        size: formatFileSize(file.file_size),
        date: formatDate(file.created_at),
        file_size: file.file_size,
        created_at: file.created_at
      }))
    } else {
      knowledgeDocuments.value = []
    }
  } catch (error) {
    console.error('加载文档列表失败:', error)
    knowledgeDocuments.value = []
  } finally {
    knowledgeLoading.value = false
  }
}

// 获取文件类型
const getFileType = (filename: string): string => {
  const ext = filename.split('.').pop()?.toLowerCase() || ''
  if (ext === 'pdf') return 'pdf'
  if (['doc', 'docx'].includes(ext)) return 'word'
  return 'text'
}

// 获取文件类型标签
const getFileTypeLabel = (filename: string): string => {
  const ext = filename.split('.').pop()?.toLowerCase() || ''
  if (ext === 'pdf') return 'PDF'
  if (['doc', 'docx'].includes(ext)) return 'Word'
  return '文本'
}

// 格式化文件大小（数据库返回的是 MB，直接显示）
const formatFileSize = (mb: number): string => {
  if (mb === 0) return '0 MB'
  return parseFloat(mb.toFixed(2)) + ' MB'
}

// 格式化日期
const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
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

// 下载文档
const downloadDoc = (doc: any) => {
  showMessage(`开始下载: ${doc.name}`, 'success')
}

// 删除文档
const deleteDoc = async (doc: any) => {
  if (!doc.file_id) {
    showMessage('文件 ID 不存在，无法删除', 'error')
    return
  }

  try {
    const token = getToken()
    const response = await fetch(`/vector/delete_file/${doc.file_id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': token || ''
      }
    })

    // 先读取响应内容
    const result = await response.json()
    console.log('删除响应:', result)

    // 检查认证错误 (包括 401 状态码和 code=0 的情况)
    if (response.status === 401 || (result.code === 0 && result.message === 'Not authenticated')) {
      checkAuthError(result)
      return
    }

    if (result.code === 1) {
      showMessage(result.message || `文件 ${doc.name} 已成功删除`, 'success')
      // 刷新文档列表
      await loadKnowledgeDocuments()
    } else {
      showMessage(result.message || '删除失败', 'error')
    }
  } catch (error) {
    console.error('删除文档失败:', error)
    showMessage('删除文档失败，请稍后重试', 'error')
  }
}

// 生成题目
const generateQuiz = async () => {
  if (!knowledgePoint.value.trim()) {
    showMessage('请输入知识点', 'error')
    return
  }

  // 验证题目数量
  const count = Math.max(1, Math.min(20, quizCount.value || 1))
  if (count !== quizCount.value) {
    quizCount.value = count
  }

  isGenerating.value = true

  try {
    const token = getToken()
    const questionType = getQuestionTypeNumber()
    
    // 构建请求体
    const requestBody = {
      question: knowledgePoint.value.trim(),
      question_type: questionType,
      question_count: count
    }
    
    console.log('=== 发送生成题目请求 ===')
    console.log('API 端点：/agent/question/generate_question')
    console.log('请求体:', requestBody)
    console.log('题型映射:', selectedQuizType.value, '→', questionType)
    
    const response = await fetch('/agent/question/generate_question', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token || ''
      },
      body: JSON.stringify(requestBody)
    })

    console.log('响应状态码:', response.status)

    // 先读取响应内容
    const result = await response.json()
    console.log('生成题目响应:', result)

    // 检查认证错误 (包括 401 状态码和 code=0 的情况)
    if (response.status === 401 || (result.code === 0 && result.message === 'Not authenticated')) {
      checkAuthError(result)
      return
    }

    if (result.code === 1 && result.data) {
      console.log('生成题目成功，原始数据:', result.data)
      
      // 解析题目数据
      // 后端可能返回 result.data.response 或 result.data.questions
      const responseData = result.data.response || result.data
      console.log('解析后的响应数据:', responseData)
      
      const questions = parseQuestionsFromResponse(responseData, questionType)
      
      if (questions.length > 0) {
        generatedQuestions.value = questions
        showMessage(`成功生成${questions.length}道${getQuestionTypeLabel(questionType)}`, 'success')
        // 清空输入框
        knowledgePoint.value = ''
        console.log('题目已显示:', questions.length, '道')
      } else {
        showMessage('题目解析失败，请检查数据格式', 'error')
      }
    } else {
      showMessage(result.message || '生成失败，请稍后重试', 'error')
    }
  } catch (error) {
    console.error('生成题目失败:', error)
    showMessage('生成题目失败，请稍后重试', 'error')
  } finally {
    isGenerating.value = false
  }
}

// 加载历史记录
const loadHistoryQuestions = async () => {
  if (isLoadingHistory.value) return
  
  isLoadingHistory.value = true
  showHistoryPanel.value = true
  
  try {
    const token = getToken()
    const response = await fetch('/agent/question/get_user_generated_questions', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token || ''
      }
    })
    
    console.log('历史记录响应状态:', response.status)
    
    if (response.status === 401) {
      try {
        const errorResult = await response.json()
        checkAuthError(errorResult)
      } catch (e) {
        console.error('解析 401 错误失败:', e)
      }
      isLoadingHistory.value = false
      return
    }
    
    const result = await response.json()
    console.log('历史记录响应:', result)
    
    // 检查认证错误
    if (result.code === 0 && result.message === 'Not authenticated') {
      checkAuthError(result)
      isLoadingHistory.value = false
      return
    }
    
    // 处理后端返回的数据格式
    if (result.code === 1 && result.data) {
      const historyData = Array.isArray(result.data) ? result.data : []
      
      // 将后端数据转换为前端格式
      historyList.value = historyData.map((item: any) => ({
        id: item.id,
        original_question: item.original_question || '', // 知识点
        generated_question_text: item.generated_question_text || '',
        question_type: item.question_type, // 0:选择题，1:填空题，2:判断题，3:主观题
        created_at: item.created_at
      }))
      
      console.log('历史记录加载成功:', historyList.value.length, '条')
    } else {
      console.log('没有历史记录')
      historyList.value = []
    }
  } catch (error) {
    console.error('加载历史记录失败:', error)
    historyList.value = []
  } finally {
    isLoadingHistory.value = false
  }
}

// 加载历史题目详情
const loadHistoryQuestion = async (history: any) => {
  console.log('=== 开始加载历史题目 ===')
  console.log('history:', history)
  console.log('history.generated_question_text:', history.generated_question_text)
  
  // 先关闭历史面板
  showHistoryPanel.value = false
  
  try {
    // 尝试解析 generated_question_text 为 JSON
    const questionData = JSON.parse(history.generated_question_text)
    console.log('解析后的题目数据:', questionData)
    
    // 解析题目
    const questions = parseQuestionsFromResponse(questionData, history.question_type)
    console.log('解析后的题目数量:', questions.length)
    
    if (questions.length > 0) {
      // 保存完整的题目数据
      currentHistoryDetail.value = {
        ...history,
        questions: questions
      }
      console.log('currentHistoryDetail 已设置:', currentHistoryDetail.value)
      
      // 打开详情弹窗
      showHistoryDetail.value = true
      console.log('showHistoryDetail 已设置为:', showHistoryDetail.value)
      
      showMessage(`已加载${questions.length}道历史题目`, 'success')
    } else {
      // 如果解析失败，尝试重新生成
      console.log('题目数量为 0，尝试重新生成')
      await regenerateHistoryQuestion(history)
    }
  } catch (parseError) {
    console.error('解析题目数据失败:', parseError)
    // 如果解析失败，尝试重新生成
    console.log('解析失败，尝试重新生成')
    await regenerateHistoryQuestion(history)
  }
}

// 关闭历史题目详情
const closeHistoryDetail = () => {
  showHistoryDetail.value = false
  currentHistoryDetail.value = null
}

// 重新生成历史题目 (备用方案)
const regenerateHistoryQuestion = async (history: any) => {
  try {
    const token = getToken()
    const response = await fetch('/agent/question/generate_question', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token || ''
      },
      body: JSON.stringify({
        question: history.original_question,
        question_type: history.question_type,
        question_count: 1
      })
    })
    
    console.log('重新生成历史题目响应状态:', response.status)
    
    if (response.status === 401) {
      try {
        const errorResult = await response.json()
        checkAuthError(errorResult)
      } catch (e) {
        console.error('解析 401 错误失败:', e)
      }
      return
    }
    
    const result = await response.json()
    console.log('重新生成历史题目响应:', result)
    
    // 检查认证错误
    if (result.code === 0 && result.message === 'Not authenticated') {
      checkAuthError(result)
      return
    }
    
    if (result.code === 1 && result.data) {
      const responseData = result.data.response || result.data
      const questions = parseQuestionsFromResponse(responseData, history.question_type)
      
      if (questions.length > 0) {
        generatedQuestions.value = questions
        showHistoryPanel.value = false
        showMessage(`已加载${questions.length}道历史题目`, 'success')
      }
    }
  } catch (error) {
    console.error('重新生成历史题目失败:', error)
    showMessage('加载历史题目失败', 'error')
  }
}

// 检测屏幕尺寸
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
  if (!isMobile.value) {
    showSidebar.value = false
  }
}

onMounted(() => {
  console.log('=== onMounted 开始执行 ===')
  console.log('currentModule:', currentModule.value)
  checkMobile()
  window.addEventListener('resize', checkMobile)
  console.log('准备加载知识库文档...')
  loadKnowledgeDocuments()
  console.log('准备加载会话列表...')
  loadChatSessions()
  
  // 从 localStorage 读取用户信息
  const userInfoStr = localStorage.getItem('userInfo')
  if (userInfoStr) {
    try {
      const userInfo = JSON.parse(userInfoStr)
      if (userInfo.username) {
        username.value = userInfo.username
      }
    } catch (e) {
      console.error('解析用户信息失败:', e)
    }
  }
  
  console.log('ChatView 已挂载')
  console.log('showAuthError 初始值:', showAuthError.value)
  console.log('authErrorMessage 初始值:', authErrorMessage.value)
  console.log('=== onMounted 执行完毕 ===')
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
  if (scrollTimeout) {
    clearTimeout(scrollTimeout)
    scrollTimeout = null
  }
})

const chatHistory = ref<Array<{
  id: number
  title: string
  created_at: string
}>>([])

const currentChatId = ref<number | null>(null)
const newSessionId = ref<string | null>(null) // 存储新建对话的 session_id

const messages = ref<Array<{
  id?: number
  role: string
  content: string
  time: string
}>>([
  {
    role: 'assistant',
    content: '你好！我是你的 AI 助手，有什么我可以帮助你的吗？',
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }
])

const selectedMessages = ref<number[]>([])
const isBatchDeleteMode = ref(false)

// 获取新的 session_id
const getNewSessionId = async (): Promise<string | null> => {
  try {
    const token = getToken()
    const response = await fetch('/agent/question/get_new_session_id', {
      method: 'GET',
      headers: {
        'Authorization': token || ''
      }
    })
    
    const result = await response.json()
    console.log('获取新 session_id 响应:', result)
    
    if (result.code === 1 && result.data) {
      newSessionId.value = result.data
      return result.data
    } else {
      console.warn('获取 session_id 失败:', result)
      return null
    }
  } catch (error) {
    console.error('获取 session_id 错误:', error)
    return null
  }
}

const startNewChat = async () => {
  try {
    const sessionId = await getNewSessionId()
    
    if (sessionId) {
      messages.value = []
      currentChatId.value = 0
      showMessage('新建会话成功', 'success')
      await loadChatSessions()
    } else {
      showMessage('新建会话失败', 'error')
    }
  } catch (error) {
    console.error('新建会话错误:', error)
    showMessage('新建会话失败', 'error')
  }
}

const selectChat = async (id: number) => {
  currentModule.value = 'qa' // 切换到智能问答模块
  currentChatId.value = id
  newSessionId.value = null // 选中历史会话时清空 newSessionId
  
  // 并行加载会话历史和刷新会话列表，减少等待时间
  await Promise.all([
    loadChatHistory(id),
    loadChatSessions()
  ])
  
  nextTick(() => {
    scrollToBottom(false, 10, 50)
  })
}

const currentModule = ref('qa') // 默认选中智能问答

// 过滤内容，移除【网络整合】及其前面的内容
const filterContent = (text: string): string => {
  const marker = '【网络整合】'
  const index = text.indexOf(marker)
  if (index !== -1) {
    return text.substring(index + marker.length)
  }
  return text
}

// Markdown 渲染函数
const renderMarkdown = (text: string) => {
  const filteredText = filterContent(text)
  return md.render(filteredText)
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isSending.value) return

  const userMessage = {
    role: 'user',
    content: inputMessage.value,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }

  messages.value.push(userMessage)
  const question = inputMessage.value
  inputMessage.value = ''
  isSending.value = true
  
  isUserScrolling.value = false
  
  // 立即滚动到最新消息（用户消息）
  nextTick(() => {
    scrollToBottom(true, 5, 100)
  })

  await sendStreamMessage(question)
}

// 流式消息发送
const sendStreamMessage = async (question: string) => {
  const aiMessage = reactive({
    role: 'assistant',
    content: '',
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  })
  messages.value.push(aiMessage)

  let buffer = ''

  try {
    let sessionId: string | number
    
    if (currentChatId.value && currentChatId.value !== 0) {
      // 选中历史会话
      sessionId = currentChatId.value
    } else if (newSessionId.value) {
      // 新建对话，使用存储的 session_id
      sessionId = newSessionId.value
    } else {
      // 没有 session_id，先获取新的 session_id
      const newId = await getNewSessionId()
      if (!newId) {
        showMessage('获取会话ID失败，请重试', 'error')
        aiMessage.content = '获取会话ID失败，请重试'
        isSending.value = false
        return
      }
      sessionId = newId
    }
    
    const token = getToken()
    const response = await fetch('/agent/question/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token || ''
      },
      body: JSON.stringify({
        question: question,
        session_id: sessionId
      })
    })

    // 检查是否是认证错误 (401 状态码)
    if (response.status === 401) {
      try {
        const errorResult = await response.json()
        console.log('401 错误响应:', errorResult)
        checkAuthError(errorResult)
      } catch (e) {
        console.error('解析 401 错误失败:', e)
      }
      aiMessage.content = '认证失败，请重新登录'
      isSending.value = false
      scrollToBottom(true, 5, 100)
      return
    }

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()

    if (!reader) {
      throw new Error('无法获取响应流')
    }

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })

      // 处理 SSE 格式的数据
      const lines = buffer.split('\n\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        const trimmedLine = line.trim()
        if (trimmedLine.startsWith('data: ')) {
          try {
            const jsonStr = trimmedLine.substring(6)
            const data = JSON.parse(jsonStr)

            // 提取 response 字段
            if (data.data && data.data.response) {
              aiMessage.content += data.data.response
              // 强制触发更新
              triggerRef(messages)
              
              // 立即滚动（不等待 nextTick）
              if (!isUserScrolling.value) {
                // 使用更频繁的小延迟滚动
                setTimeout(() => {
                  scrollToBottom(false, 3, 50)
                }, 0)
              }
            }

            // 检查是否结束
            if (data.data && data.data.done) {
              break
            }
          } catch (e) {
            console.error('解析 SSE 数据失败:', e)
          }
        } else if (trimmedLine.startsWith('event: done')) {
          break
        }
      }

      // 流式输出过程中，智能自动滚动（仅当用户未手动滚动时）
      nextTick(() => {
        if (!isUserScrolling.value) {
          scrollToBottom(false, 3, 50)
        }
      })
    }

    // 处理剩余缓冲区
    if (buffer.trim()) {
      const trimmedLine = buffer.trim()
      if (trimmedLine.startsWith('data: ')) {
        try {
          const jsonStr = trimmedLine.substring(6)
          const data = JSON.parse(jsonStr)
          if (data.data && data.data.response) {
            aiMessage.content += data.data.response
            triggerRef(messages)
          }
        } catch (e) {
          console.error('解析剩余 SSE 数据失败:', e)
        }
      }
    }
  } catch (error) {
    console.error('Stream message error:', error)
    aiMessage.content = '连接服务器失败，请稍后重试'
  } finally {
    isSending.value = false
    
    // 流式输出完成后，确保滚动到底部
    nextTick(() => {
      scrollToBottom(true, 5, 100)
    })
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.chat-page {
  display: flex;
  height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #F5F8FF 0%, #E8EFFF 50%, #F0F6FF 100%);
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

/* 左侧边栏 */
.sidebar {
  width: 280px;
  min-width: 280px;
  max-width: 320px;
  flex-shrink: 0;
  background: #FFFFFF;
  border-right: 1px solid #D4DDFD;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  overflow: hidden;
  box-shadow: 2px 0 12px rgba(166, 189, 251, 0.1);
}

.sidebar.collapsed {
  width: 80px;
  min-width: 80px;
  max-width: 80px;
}

.sidebar-header {
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #D4DDFD;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 700;
  color: #A6BDFB;
}

.logo svg {
  width: 32px;
  height: 32px;
}

.new-chat-btn {
  margin: 12px 16px 20px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  border: none;
  border-radius: 12px;
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(166, 189, 251, 0.35);
}

.new-chat-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(166, 189, 251, 0.45);
  background: linear-gradient(135deg, #8FA8F5 0%, #7896F0 100%);
}

.new-chat-btn svg {
  width: 20px;
  height: 20px;
}

/* 功能模块样式 */
.function-modules {
  padding: 20px 16px;
  background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFF 100%);
}

.module-title {
  font-size: 11px;
  color: #A6BDFB;
  margin-bottom: 16px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding-left: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.module-title::before {
  content: '';
  width: 3px;
  height: 12px;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  border-radius: 2px;
}

.module-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.module-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid #D4DDFD;
  background: #FFFFFF;
  position: relative;
  overflow: hidden;
}

.module-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  transform: scaleY(0);
  transition: transform 0.3s ease;
  border-radius: 12px 0 0 12px;
}

.module-item:hover::before {
  transform: scaleY(1);
}

.module-item:hover {
  background: linear-gradient(135deg, #F5F8FF 0%, #FFFFFF 100%);
  border-color: #A6BDFB;
  transform: translateX(6px);
  box-shadow: 0 4px 16px rgba(166, 189, 251, 0.2);
}

.module-item:active {
  transform: translateX(6px) scale(0.98);
}

.module-item.active {
  background: linear-gradient(135deg, #E8EFFF 0%, #F0F6FF 100%);
  border-color: #A6BDFB;
  border-width: 3px;
  box-shadow: 0 6px 20px rgba(166, 189, 251, 0.3), inset 0 0 0 1px rgba(166, 189, 251, 0.1);
}

.module-item.active::before {
  transform: scaleY(1);
}

.module-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #F5F8FF 0%, #E8EFFF 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 2px 4px rgba(166, 189, 251, 0.15);
  position: relative;
}

.module-icon::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 12px;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.module-icon svg {
  width: 22px;
  height: 22px;
  color: #A6BDFB;
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}

.module-item:hover .module-icon {
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  box-shadow: 0 6px 16px rgba(166, 189, 251, 0.4);
  transform: scale(1.05) rotate(-5deg);
}

.module-item:hover .module-icon::after {
  opacity: 1;
}

.module-item:hover .module-icon svg {
  color: #FFFFFF;
  transform: scale(1.1);
}

.module-item.active .module-icon {
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  box-shadow: 0 4px 12px rgba(166, 189, 251, 0.3);
}

.module-item.active .module-icon svg {
  color: #FFFFFF;
}

.module-info {
  flex: 1;
  min-width: 0;
}

.module-name {
  font-size: 14px;
  font-weight: 600;
  color: #5A7BD6;
  margin-bottom: 3px;
  transition: color 0.3s ease;
}

.module-item:hover .module-name {
  color: #4A6BC6;
}

.module-item.active .module-name {
  color: #4A6BC6;
  font-weight: 700;
}

.module-desc {
  font-size: 11px;
  color: #A6BDFB;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 500;
  transition: color 0.3s ease;
}

.module-item:hover .module-desc {
  color: #8A9FD8;
}

.module-item.active .module-desc {
  color: #7A8FD0;
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 0;
  background: transparent;
}

.history-title {
  font-size: 14px;
  color: #1F2937;
  margin-bottom: 12px;
  font-weight: 600;
  padding: 0 12px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.history-item {
  padding: 12px 14px;
  border-radius: 8px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #1F2937;
  font-size: 14px;
  line-height: 1.5;
  overflow: hidden;
  border: 1px solid transparent;
  justify-content: flex-start;
  background: transparent;
  margin-bottom: 4px;
  position: relative;
}

.history-item:hover {
  background: #F9FAFB;
  border-color: #E5E7EB;
}

.history-item.active {
  background: #EEF2FF;
  border-color: #6366F1;
  box-shadow: 0 2px 4px rgba(99, 102, 241, 0.1);
}

.history-item svg {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  color: #6B7280;
  margin-top: 2px;
}

.history-item.active svg {
  color: #4F46E5;
}

.chat-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
  overflow: hidden;
  min-width: 0;
}

.chat-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: left;
  color: #111827;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.4;
}

.chat-time {
  font-size: 12px;
  color: #9CA3AF;
  text-align: left;
  line-height: 1;
}

.history-item .delete-btn {
  display: none;
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 28px;
  height: 28px;
  padding: 4px;
  background: #FEE2E2;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: #EF4444;
  transition: all 0.2s ease;
}

.history-item:hover .delete-btn {
  display: flex;
  align-items: center;
  justify-content: center;
}

.history-item .delete-btn:hover {
  background: #FECACA;
  transform: translateY(-50%) scale(1.1);
}

.history-item .delete-btn svg {
  width: 16px;
  height: 16px;
}

.history-item.active .chat-title {
  color: #312E81;
  font-weight: 600;
}

.history-item.active .chat-time {
  color: #6366F1;
}

.history-item:hover {
  background: #F3F4F6;
}

.history-item.active {
  border: 2px solid #4F46E5;
  background: #E5E7EB;
  font-weight: 600;
  border-radius: 8px;
}

.history-item.active span {
  color: #111827;
  font-weight: 700;
}

/* 智能出题题目类型选择栏 */
.quiz-type-bar {
  padding: 16px 24px;
  background: #FFFFFF;
  border-bottom: 1px solid #E8EFFF;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 历史按钮 */
.history-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: #FFFFFF;
  border: 2px solid #D4DDFD;
  border-radius: 10px;
  color: #5A7BD6;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: relative;
}

.history-btn svg {
  width: 18px;
  height: 18px;
}

.history-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  color: #FFFFFF;
  border-color: transparent;
  box-shadow: 0 4px 15px rgba(166, 189, 251, 0.3);
  transform: translateY(-2px);
}

.history-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.history-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background: linear-gradient(135deg, #FF6B6B 0%, #EE5A6F 100%);
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(255, 107, 107, 0.4);
}

/* 历史记录面板 */
.history-panel {
  position: absolute;
  top: 60px;
  right: 24px;
  width: 600px;
  max-height: 700px;
  background: #FFFFFF;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  border: 2px solid #E8EFFF;
  z-index: 1000;
  overflow: hidden;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32px 32px;
  background: linear-gradient(135deg, #F8FAFF 0%, #F0F4FF 100%);
  border-bottom: 2px solid #E8EFFF;
}

.history-header h3 {
  font-size: 22px;
  font-weight: 700;
  color: #2D3748;
  margin: 0;
  letter-spacing: 0.5px;
}

.close-btn {
  width: 44px;
  height: 44px;
  border: none;
  background: #FFFFFF;
  border-radius: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4A5568;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.close-btn svg {
  width: 26px;
  height: 26px;
}

.close-btn:hover {
  background: linear-gradient(135deg, #FF6B6B 0%, #EE5A6F 100%);
  color: #FFFFFF;
  transform: rotate(90deg);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
}

.history-list {
  max-height: 550px;
  overflow-y: auto;
  padding: 28px 32px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 26px 28px;
  background: #F8FAFF;
  border-radius: 18px;
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
}

.history-item:last-child {
  margin-bottom: 0;
}

.history-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.history-info {
  flex: 1;
  min-width: 0;
  margin-right: 20px;
  text-align: left;
}

.history-title {
  font-size: 14px;
  font-weight: 600;
  color: #2D3748;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  letter-spacing: 0.3px;
  text-align: left;
}

.history-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #718096;
  align-items: center;
  justify-content: flex-start;
}

.history-type {
  background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
  color: #1976D2;
  padding: 4px 10px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 12px;
  box-shadow: 0 2px 4px rgba(25, 118, 210, 0.1);
}

.history-count {
  background: #EDF2F7;
  color: #4A5568;
  padding: 4px 10px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 12px;
}

.history-date {
  font-size: 12px;
  color: #A0AEC0;
  font-weight: 500;
  white-space: nowrap;
  min-width: 80px;
  text-align: right;
}

.history-arrow {
  width: 20px;
  height: 20px;
  color: #A0AEC0;
  flex-shrink: 0;
  margin-left: 12px;
  transition: all 0.3s ease;
}

.history-item:hover .history-arrow {
  color: #5A7BD6;
  transform: translateX(4px);
}

.history-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #A0AEC0;
}

.history-empty svg {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.history-empty p {
  font-size: 15px;
  margin: 0;
  color: #718096;
}

/* 历史题目详情弹窗 */
.history-detail-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10001;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.3s ease;
}

.history-detail-modal {
  width: 90%;
  max-width: 800px;
  max-height: 85vh;
  background: #FFFFFF;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  display: flex;
  flex-direction: column;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: linear-gradient(135deg, #F8FAFF 0%, #F0F4FF 100%);
  border-bottom: 2px solid #E8EFFF;
}

.detail-header h3 {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #2D3748;
  flex: 1;
}

.detail-type-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.detail-type-badge.type-choice {
  background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
  color: #1976D2;
}

.detail-type-badge.type-fill {
  background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%);
  color: #7B1FA2;
}

.detail-type-badge.type-truefalse {
  background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
  color: #388E3C;
}

.detail-type-badge.type-subjective {
  background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
  color: #F57C00;
}

.detail-title {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.detail-header .close-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: #FFFFFF;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4A5568;
  transition: all 0.3s ease;
  flex-shrink: 0;
  margin-left: 12px;
}

.detail-header .close-btn:hover {
  background: linear-gradient(135deg, #FF6B6B 0%, #EE5A6F 100%);
  color: #FFFFFF;
  transform: rotate(90deg);
}

.detail-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #F8FAFF;
}

.detail-question-card {
  background: #FFFFFF;
  border-radius: 14px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border: 2px solid #B8C9F5;
}

.detail-question-card:last-child {
  margin-bottom: 0;
}

.detail-question-header {
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #F0F4FF;
  text-align: left;
}

.detail-question-text {
  font-size: 15px;
  line-height: 1.8;
  color: #2D3748;
  font-weight: 500;
  margin-bottom: 16px;
  text-align: left;
}

.detail-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.detail-option-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  background: #F8FAFF;
  border-radius: 10px;
  border: 2px solid #B8C9F5;
  transition: all 0.3s ease;
  text-align: left;
}

.detail-option-item:hover {
  background: #FFFFFF;
  border-color: #5A7BD6;
  box-shadow: 0 2px 10px rgba(166, 189, 251, 0.2);
}

.detail-option-item .option-label {
  font-weight: 700;
  color: #5A7BD6;
  min-width: 24px;
  flex-shrink: 0;
  font-size: 15px;
}

.detail-option-item .option-content {
  flex: 1;
  color: #4A5568;
  line-height: 1.6;
  font-size: 14px;
  text-align: left;
}

.detail-answer-section {
  margin-top: 16px;
  padding: 16px;
  background: linear-gradient(135deg, #F8FAFF 0%, #F0F4FF 100%);
  border-radius: 12px;
  border-left: 4px solid #5A7BD6;
}

.detail-answer-section .answer-label {
  font-weight: 700;
  color: #5A7BD6;
  font-size: 14px;
  margin-bottom: 8px;
  text-align: left;
}

.detail-answer-section .answer-value {
  color: #2D3748;
  font-weight: 600;
  font-size: 15px;
  padding: 6px 12px;
  background: #FFFFFF;
  border-radius: 6px;
  border: 2px solid #B8C9F5;
  display: inline-block;
}

.detail-explanation {
  color: #4A5568;
  line-height: 1.8;
  font-size: 14px;
  background: #FFFFFF;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #B8C9F5;
  text-align: left;
}

/* 弹窗动画 */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .history-detail-modal,
.modal-leave-to .history-detail-modal {
  transform: scale(0.9) translateY(20px);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* 知识点输入区域 */
.knowledge-input-section {
  padding: 16px 24px;
  background: #F5F8FF;
  border-bottom: 1px solid #E8EFFF;
  margin-bottom: 20px;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  color: #5A7BD6;
  font-weight: 600;
  font-size: 14px;
}

.input-label svg {
  width: 18px;
  height: 18px;
}

.knowledge-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.knowledge-input {
  width: 100%;
  padding: 12px 16px;
  background: #FFFFFF;
  border: 2px solid #D4DDFD;
  border-radius: 12px;
  font-size: 14px;
  color: #2D3748;
  outline: none;
  transition: all 0.3s ease;
  resize: vertical;
  line-height: 1.5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.knowledge-input:focus {
  border-color: #A6BDFB;
  box-shadow: 0 0 0 4px rgba(166, 189, 251, 0.1), 0 4px 12px rgba(166, 189, 251, 0.15);
}

.knowledge-input::placeholder {
  color: #A0AEC0;
}

/* 题目显示区域 */
.questions-display-section {
  padding: 24px;
  background: #F8FAFF;
  border-radius: 16px;
  margin: 20px 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.questions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #E1E8FF;
}

.questions-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: #2D3748;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.questions-header h2::before {
  content: '';
  width: 4px;
  height: 24px;
  background: linear-gradient(180deg, #A6BDFB 0%, #7896F0 100%);
  border-radius: 2px;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: #FFFFFF;
  border: 2px solid #A6BDFB;
  border-radius: 10px;
  color: #5A7BD6;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(166, 189, 251, 0.15);
}

.export-btn svg {
  width: 18px;
  height: 18px;
}

.export-btn:hover {
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  color: #FFFFFF;
  border-color: transparent;
  box-shadow: 0 4px 15px rgba(166, 189, 251, 0.35);
  transform: translateY(-2px);
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-card {
  background: #FFFFFF;
  border-radius: 14px;
  padding: 24px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border: 2px solid #B8C9F5;
  transition: all 0.3s ease;
}

.question-card:hover {
  box-shadow: 0 6px 25px rgba(166, 189, 251, 0.25);
  border-color: #5A7BD6;
  transform: translateY(-2px);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #F0F4FF;
}

.question-number {
  font-size: 15px;
  font-weight: 700;
  color: #2D3748;
}

.question-type-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.question-type-badge.type-choice {
  background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
  color: #1976D2;
}

.question-type-badge.type-fill {
  background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%);
  color: #7B1FA2;
}

.question-type-badge.type-truefalse {
  background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
  color: #388E3C;
}

.question-type-badge.type-subjective {
  background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
  color: #F57C00;
}

.question-content {
  margin-bottom: 20px;
}

.question-text {
  font-size: 15px;
  line-height: 1.8;
  color: #2D3748;
  font-weight: 500;
  margin-bottom: 16px;
  text-align: left;
}

.question-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.option-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  background: #F8FAFF;
  border-radius: 10px;
  border: 2px solid #E8EFFF;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.option-item:hover {
  background: #FFFFFF;
  border-color: #A6BDFB;
  box-shadow: 0 2px 10px rgba(166, 189, 251, 0.1);
}

/* 正确答案样式 */
.option-item.option-correct {
  background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
  border-color: #4CAF50;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.25);
}

.option-item.option-correct:hover {
  background: linear-gradient(135deg, #C8E6C9 0%, #A5D6A7 100%);
  border-color: #43A047;
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.35);
}

/* 错误答案样式 */
.option-item.option-wrong {
  background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
  border-color: #EF5350;
  box-shadow: 0 4px 15px rgba(239, 83, 80, 0.25);
}

.option-item.option-wrong:hover {
  background: linear-gradient(135deg, #FFCDD2 0%, #EF9A9A 100%);
  border-color: #E53935;
  box-shadow: 0 6px 20px rgba(239, 83, 80, 0.35);
}

.option-label {
  font-weight: 700;
  color: #5A7BD6;
  min-width: 24px;
  flex-shrink: 0;
  font-size: 15px;
}

.option-content {
  flex: 1;
  color: #4A5568;
  line-height: 1.6;
  font-size: 14px;
  text-align: left;
}

.option-status {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.option-status svg {
  width: 22px;
  height: 22px;
}

.option-correct .option-status svg {
  color: #2E7D32;
}

.option-wrong .option-status svg {
  color: #C62828;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .question-options {
    grid-template-columns: 1fr;
  }
  
  .questions-display-section {
    margin: 16px;
    padding: 16px;
  }
  
  .question-card {
    padding: 16px;
  }
}

/* 判断题按钮样式 */
.true-false-buttons {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #F0F4FF;
}

.tf-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 28px;
  border: 2px solid #D4DDFD;
  border-radius: 10px;
  background: #FFFFFF;
  color: #2D3748;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.tf-btn svg {
  width: 20px;
  height: 20px;
  opacity: 0;
  transform: scale(0);
  transition: all 0.3s ease;
  color: currentColor;
}

.tf-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.tf-btn.tf-true:hover {
  border-color: #81C784;
  background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%);
}

.tf-btn.tf-false:hover {
  border-color: #E57373;
  background: linear-gradient(135deg, #FFEBEE 0%, #FBE9E7 100%);
}

/* 选中正确答案 - 绿色背景，白色文字，正常绿色边框 */
.tf-btn.tf-correct {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.4) 0%, rgba(129, 199, 132, 0.5) 100%);
  border-color: #2E7D32;
  color: #FFFFFF;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.5);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.tf-btn.tf-correct svg {
  opacity: 1;
  transform: scale(1);
  color: #FFFFFF;
}

.tf-btn.tf-correct:hover {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.5) 0%, rgba(129, 199, 132, 0.6) 100%);
  border-color: #1B5E20;
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.6);
}

/* 选中错误答案 - 红色背景，白色文字，正常红色边框 */
.tf-btn.tf-wrong {
  background: linear-gradient(135deg, rgba(239, 83, 80, 0.4) 0%, rgba(229, 115, 115, 0.5) 100%);
  border-color: #C62828;
  color: #FFFFFF;
  box-shadow: 0 4px 15px rgba(239, 83, 80, 0.5);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.tf-btn.tf-wrong svg {
  opacity: 1;
  transform: scale(1);
  color: #FFFFFF;
}

.tf-btn.tf-wrong:hover {
  background: linear-gradient(135deg, rgba(239, 83, 80, 0.5) 0%, rgba(229, 115, 115, 0.6) 100%);
  border-color: #B71C1C;
  box-shadow: 0 6px 20px rgba(239, 83, 80, 0.6);
}

/* 填空题输入区域 */
.fill-input-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #F0F4FF;
}

.fill-input-wrapper {
  display: flex;
  gap: 12px;
  align-items: center;
  max-width: 600px;
}

.fill-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #D4DDFD;
  border-radius: 10px;
  font-size: 15px;
  color: #2D3748;
  outline: none;
  transition: all 0.3s ease;
  background: #FFFFFF;
}

.fill-input:focus {
  border-color: #A6BDFB;
  box-shadow: 0 0 0 4px rgba(166, 189, 251, 0.1);
}

.fill-input:disabled {
  background: #F8FAFF;
  color: #4A5568;
  cursor: not-allowed;
}

/* 填空题答案正确 */
.fill-input.fill-correct {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(129, 199, 132, 0.25) 100%);
  border-color: #4CAF50;
  color: #1B5E20;
  font-weight: 600;
}

/* 填空题答案错误 */
.fill-input.fill-wrong {
  background: linear-gradient(135deg, rgba(239, 83, 80, 0.15) 0%, rgba(229, 115, 115, 0.25) 100%);
  border-color: #EF5350;
  color: #C62828;
  font-weight: 600;
}

/* 提交按钮 */
.submit-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  border: none;
  border-radius: 10px;
  color: #FFFFFF;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(166, 189, 251, 0.3);
  flex-shrink: 0;
}

.submit-btn svg {
  width: 20px;
  height: 20px;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(166, 189, 251, 0.45);
  background: linear-gradient(135deg, #8FA8F5 0%, #7896F0 100%);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 8px rgba(166, 189, 251, 0.15);
}

/* 提交状态图标 */
.submit-status {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  animation: scaleIn 0.3s ease;
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.submit-status svg {
  width: 24px;
  height: 24px;
}

.submit-status.fill-correct {
  background: linear-gradient(135deg, #4CAF50 0%, #43A047 100%);
  color: #FFFFFF;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
}

.submit-status.fill-wrong {
  background: linear-gradient(135deg, #EF5350 0%, #E53935 100%);
  color: #FFFFFF;
  box-shadow: 0 4px 15px rgba(239, 83, 80, 0.4);
}

.question-footer {
  border-top: 1px solid #F0F4FF;
  padding-top: 16px;
}

.show-answer-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: #F8FAFF;
  border: 2px solid #D4DDFD;
  border-radius: 10px;
  color: #5A7BD6;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.show-answer-btn svg {
  width: 18px;
  height: 18px;
}

.show-answer-btn:hover {
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  color: #FFFFFF;
  border-color: transparent;
  box-shadow: 0 4px 15px rgba(166, 189, 251, 0.3);
  transform: translateY(-2px);
}

.answer-section {
  margin-top: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #F8FAFF 0%, #F0F4FF 100%);
  border-radius: 12px;
  border-left: 4px solid #A6BDFB;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.answer-item {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
  align-items: flex-start;
}

.answer-item:last-child {
  margin-bottom: 0;
}

.answer-label {
  font-weight: 700;
  color: #5A7BD6;
  min-width: 80px;
  flex-shrink: 0;
  font-size: 14px;
  padding-top: 2px;
}

.answer-value {
  color: #2D3748;
  font-weight: 600;
  font-size: 15px;
  padding: 6px 12px;
  background: #FFFFFF;
  border-radius: 6px;
  border: 2px solid #D4DDFD;
  text-align: left;
}

.answer-explanation {
  flex: 1;
  color: #4A5568;
  line-height: 1.8;
  font-size: 14px;
  background: #FFFFFF;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #E8EFFF;
  text-align: left;
}

.generate-controls {
  display: flex;
  gap: 20px;
  align-items: flex-end;
  margin-top: 8px;
  justify-content: space-between;
}

.quiz-count-input {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-shrink: 0;
}

.count-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 600;
  color: #5A7BD6;
}

.label-icon {
  width: 14px;
  height: 14px;
  opacity: 0.8;
}

.count-input-wrapper {
  display: flex;
  align-items: center;
  gap: 0;
  background: #FFFFFF;
  border: 2px solid #D4DDFD;
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(166, 189, 251, 0.08);
  height: 36px;
}

.count-input-wrapper:focus-within {
  border-color: #A6BDFB;
  box-shadow: 0 0 0 3px rgba(166, 189, 251, 0.12), 0 3px 10px rgba(166, 189, 251, 0.15);
}

.count-btn {
  width: 30px;
  height: 36px;
  border: none;
  background: #F5F8FF;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #5A7BD6;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.count-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  color: #FFFFFF;
}

.count-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  background: #F5F8FF;
}

.count-btn svg {
  width: 14px;
  height: 14px;
  transition: transform 0.2s ease;
}

.count-btn:hover:not(:disabled) svg {
  transform: scale(1.1);
}

.count-input {
  width: 45px;
  height: 36px;
  border: none;
  background: transparent;
  font-size: 14px;
  font-weight: 700;
  color: #5A6B8A;
  outline: none;
  text-align: center;
  flex-shrink: 0;
}

.count-input:focus {
  background: rgba(166, 189, 251, 0.05);
}

.count-input::-webkit-inner-spin-button,
.count-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.count-input[type=number] {
  -moz-appearance: textfield;
}

.knowledge-input {
  width: 100%;
  padding: 14px;
  background: #FFFFFF;
  border: 2px solid #D4DDFD;
  border-radius: 12px;
  font-size: 14px;
  color: #5A6B8A;
  outline: none;
  resize: vertical;
  min-height: 100px;
  transition: all 0.3s ease;
}

.knowledge-input:focus {
  border-color: #A6BDFB;
  box-shadow: 0 0 0 4px rgba(166, 189, 251, 0.1);
}

.knowledge-input::placeholder {
  color: #A6BDFB;
  opacity: 0.6;
}

.generate-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 28px;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  border: none;
  border-radius: 12px;
  color: #FFFFFF;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(166, 189, 251, 0.35);
  flex-shrink: 0;
  height: 40px;
  position: relative;
  overflow: hidden;
}

.generate-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.generate-btn:hover:not(:disabled)::before {
  left: 100%;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(166, 189, 251, 0.5);
  background: linear-gradient(135deg, #8FA8F5 0%, #7896F0 100%);
}

.generate-btn:active:not(:disabled) {
  transform: translateY(-1px);
}

.generate-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 4px 15px rgba(166, 189, 251, 0.2);
}

.generate-btn svg {
  width: 18px;
  height: 18px;
  transition: all 0.3s ease;
}

.generate-btn:hover:not(:disabled) svg {
  transform: scale(1.1) rotate(-10deg);
}

.type-options {
  display: flex;
  justify-content: center;
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.type-option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: #F5F8FF;
  border: 2px solid #D4DDFD;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 14px;
  font-weight: 500;
  color: #6B7280;
  flex: 0 0 auto;
}

.type-option svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.type-option:hover {
  background: #E8F0FF;
  border-color: #A6BDFB;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(166, 189, 251, 0.2);
}

.type-option:hover svg {
  color: #5A7BD6;
  transform: scale(1.1);
}

.type-option.active {
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  border-color: #5A7BD6;
  color: #FFFFFF;
  box-shadow: 0 4px 15px rgba(90, 123, 214, 0.35);
}

.type-option.active svg {
  color: #FFFFFF;
}

.type-option.active:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(90, 123, 214, 0.45);
}

.history-item:hover {
  background: #F5F8FF;
  border-color: #D4DDFD;
}

.history-item.active {
  background: rgba(255, 255, 255, 0.12);
  color: #FFFFFF;
  font-weight: 500;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #D4DDFD;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #5A7BD6;
  font-size: 14px;
  font-weight: 600;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(166, 189, 251, 0.35);
}

/* 知识库模块 */
.knowledge-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #F5F8FF 0%, #FFFFFF 100%);
  height: 100vh;
  overflow: hidden;
}

.knowledge-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  position: relative;
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  padding: 24px;
  background: #FFFFFF;
  border: 2px solid #E8EFFF;
  border-radius: 16px;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: #A6BDFB;
  box-shadow: 0 4px 16px rgba(166, 189, 251, 0.15);
  transform: translateY(-2px);
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #8A9FD8;
}

/* 搜索栏 */
.search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.search-input-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  width: 20px;
  height: 20px;
  color: #A6BDFB;
}

.search-input {
  width: 100%;
  padding: 14px 16px 14px 44px;
  background: #FFFFFF;
  border: 2px solid #D4DDFD;
  border-radius: 12px;
  font-size: 14px;
  color: #5A6B8A;
  outline: none;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #A6BDFB;
  box-shadow: 0 0 0 4px rgba(166, 189, 251, 0.1);
}

.search-input::placeholder {
  color: #A6BDFB;
  opacity: 0.6;
}

.upload-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  border: none;
  border-radius: 12px;
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(166, 189, 251, 0.3);
  white-space: nowrap;
}

.upload-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(166, 189, 251, 0.4);
}

.upload-btn svg {
  width: 20px;
  height: 20px;
}

/* 刷新按钮 */
.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 20px;
  background: #FFFFFF;
  border: 1px solid #D4DDFD;
  border-radius: 12px;
  color: #5A7BD6;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.refresh-btn:hover:not(:disabled) {
  background: #F5F8FF;
  border-color: #A6BDFB;
  transform: translateY(-2px);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-btn svg {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.refresh-btn svg.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 文档列表 */
.document-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #E8EFFF;
  border-top-color: #A6BDFB;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  font-size: 14px;
  color: #8A9FD8;
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
}

.document-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: #FFFFFF;
  border: 1px solid #E8EFFF;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.document-item:hover {
  border-color: #A6BDFB;
  box-shadow: 0 4px 12px rgba(166, 189, 251, 0.1);
}

.doc-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.doc-icon.pdf {
  background: linear-gradient(135deg, #FFE5E5 0%, #FFF0F0 100%);
}

.doc-icon.word {
  background: linear-gradient(135deg, #E5F0FF 0%, #F0F7FF 100%);
}

.doc-icon.text {
  background: linear-gradient(135deg, #E5FFE5 0%, #F0FFF0 100%);
}

.doc-icon svg {
  width: 24px;
  height: 24px;
}

.doc-icon.pdf svg {
  color: #FF6B6B;
}

.doc-icon.word svg {
  color: #4A90E2;
}

.doc-icon.text svg {
  color: #50C878;
}

.doc-info {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #8A9FD8;
  min-width: 120px;
}

.doc-type {
  font-weight: 600;
}

.doc-name {
  flex: 1;
  font-size: 15px;
  font-weight: 600;
  color: #5A6B8A;
}

.doc-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border: 1px solid #D4DDFD;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #FFFFFF;
  color: #6B7280;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.action-btn svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  transition: all 0.3s ease;
  stroke-width: 2.5;
}

.action-btn:hover {
  background: #F9FAFB;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: rgba(0, 0, 0, 0.08);
  transform: translateY(-1px);
}

.action-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.action-btn:hover svg {
  transform: scale(1.05);
  color: #5A7BD6;
}

.action-btn.delete {
  border-color: #FECDD3;
}

.action-btn.delete:hover {
  border-color: #F87171;
  background: #FEF2F2;
}

.action-btn.delete:hover svg {
  color: #EF4444;
}

/* 主聊天区域 */
.chat-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  background: #FFFFFF;
  height: 100vh;
  overflow: hidden;
}

.chat-header {
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #D4DDFD;
  background: #FFFFFF;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.model-selector {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #F5F8FF;
  border: 1px solid #D4DDFD;
  border-radius: 8px;
  color: #5A7BD6;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.model-selector:hover {
  background: #E8EFFF;
  border-color: #A6BDFB;
}

.model-selector svg {
  width: 16px;
  height: 16px;
  color: #A6BDFB;
}

.header-right {
  display: flex;
  gap: 8px;
}

.header-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #657166;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.header-btn:hover {
  background: #F5F9FA;
  color: #5BA3C9;
}

.header-btn svg {
  width: 20px;
  height: 20px;
}

.batch-delete-icon {
  width: 20px;
  height: 20px;
}

.batch-delete-icon .rect-bg {
  fill: rgba(111, 179, 198, 0.15);
  stroke: #6FB3C6;
  stroke-width: 1.5;
  transition: all 0.3s ease;
}

.batch-delete-icon .x-line {
  stroke: #6FB3C6;
  stroke-width: 2;
  stroke-linecap: round;
  transition: all 0.3s ease;
}

.header-btn:hover .batch-delete-icon .rect-bg {
  fill: rgba(111, 179, 198, 0.3);
  stroke: #5BA3C9;
}

.header-btn:hover .batch-delete-icon .x-line {
  stroke: #5BA3C9;
}

.batch-delete-btn {
  position: relative;
  background: #FEE2E2;
  color: #EF4444;
}

.batch-delete-btn:hover {
  background: #FECACA;
}

.batch-delete-count {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #EF4444;
  color: white;
  font-size: 10px;
  font-weight: bold;
  min-width: 16px;
  height: 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}

.cancel-batch-btn {
  margin-left: 4px;
}

.delete-message-btn {
  color: #EF4444;
}

.delete-message-btn:hover {
  background: #FEE2E2;
  color: #DC2626;
}

/* 聊天内容区域 */
.chat-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  min-height: 0;
}

.welcome-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #5A7BD6;
  text-align: center;
}

.welcome-message h1 {
  font-size: 32px;
  margin-bottom: 12px;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.welcome-message p {
  font-size: 16px;
  color: #8A9FD8;
}

.messages-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 765px;
  margin: 0 auto;
  width: 100%;
}

.message {
  display: flex;
  gap: 12px;
  animation: messageSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  align-items: flex-start;
}

.message-checkbox {
  position: absolute;
  left: -40px;
  top: 12px;
  transform: none;
  width: 24px;
  height: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 1;
  transition: all 0.2s ease;
  z-index: 10;
  align-self: flex-start;
}

.message-checkbox svg {
  width: 20px;
  height: 20px;
  transition: all 0.2s ease;
}

/* 批量删除模式下，未选中的复选框显示红色边框 */
.message-checkbox:not(.checked) svg rect {
  stroke: #EF4444;
  stroke-width: 2;
}

/* 批量删除模式下，未选中的复选框悬停时显示红色背景 */
.message-checkbox:not(.checked):hover svg rect {
  fill: rgba(239, 68, 68, 0.1);
}

/* 选中的复选框 */
.message-checkbox.checked svg rect {
  fill: #EF4444;
  stroke: #EF4444;
}

.message-checkbox.checked svg {
  filter: drop-shadow(0 0 2px rgba(239, 68, 68, 0.5));
}

.message.selected {
  background: rgba(99, 102, 241, 0.1);
  border-radius: 8px;
  padding: 4px;
  margin: -4px;
}

.message-delete-checkbox {
  position: relative;
  right: auto;
  top: auto;
  transform: none;
  width: 24px;
  height: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
  z-index: 100;
  flex-shrink: 0;
  margin-left: 8px;
}

.is-batch-mode .message-delete-checkbox,
.message.selected .message-delete-checkbox {
  opacity: 1;
}

.message-delete-checkbox svg {
  width: 20px;
  height: 20px;
}

.message-delete-checkbox.checked {
  transform: scale(1.1);
}

@keyframes messageSlideIn {
  from {
    opacity: 0;
    transform: translateY(15px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
  align-self: flex-start;
}

.message-avatar svg {
  width: 32px;
  height: 32px;
}

.message-content {
  max-width: 85%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
}

.message.user .message-content {
  max-width: 85%;
  align-items: flex-end;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.message.user .message-header {
  flex-direction: row-reverse;
}

.message-name {
  font-size: 14px;
  font-weight: 600;
  color: #5A7BD6;
}

.message-time {
  font-size: 12px;
  color: #A6BDFB;
}

.message.assistant .message-text {
  background: linear-gradient(135deg, #F8FAFF 0%, #FFFFFF 100%);
  border-radius: 18px;
  border-bottom-left-radius: 4px;
  border: 1px solid #E8EFFF;
  box-shadow: 0 2px 8px rgba(166, 189, 251, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.message.assistant .message-text:hover {
  box-shadow: 0 4px 16px rgba(166, 189, 251, 0.15);
  transform: translateY(-1px);
}

.message.user .message-text {
  background: linear-gradient(135deg, #6B8DFF 0%, #5A7BD6 100%);
  color: #FFFFFF;
  border-radius: 18px;
  border-bottom-right-radius: 4px;
  box-shadow: 0 4px 16px rgba(107, 141, 255, 0.35);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 10px 14px;
  text-align: left;
}

.message.user .message-text:hover {
  box-shadow: 0 6px 24px rgba(107, 141, 255, 0.45);
  transform: translateY(-2px);
}

.message-actions {
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.message.assistant:hover .message-actions {
  opacity: 1;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8A9A9A;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: #F5F9FA;
  color: #5BA3C9;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

/* 等待动画样式 */
.thinking-inline {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-left: 8px;
  padding: 2px 8px;
  background: linear-gradient(135deg, #E8EFFF 0%, #F0F6FF 100%);
  border-radius: 10px;
  border: 1px solid #D4DDFD;
}

.thinking-text-small {
  font-size: 11px;
  color: #5A7BD6;
  font-weight: 500;
}

.thinking-dots-inline {
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.thinking-dots-inline span {
  width: 4px;
  height: 4px;
  background: #A6BDFB;
  border-radius: 50%;
  animation: thinkingBounceInline 1.4s ease-in-out infinite;
}

.thinking-dots-inline span:nth-child(1) {
  animation-delay: 0s;
}

.thinking-dots-inline span:nth-child(2) {
  animation-delay: 0.2s;
}

.thinking-dots-inline span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes thinkingBounceInline {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-3px);
    opacity: 1;
  }
}

/* Markdown 内容样式 */
.message.assistant .message-text {
  padding: 10px 14px;
  font-size: 15px;
  line-height: 1.6;
  color: #4A5568;
  text-align: left;
  word-break: break-word;
}

.message.assistant .message-text :deep(p) {
  margin: 4px 0;
  line-height: 1.7;
}

.message.assistant .message-text :deep(h1),
.message.assistant .message-text :deep(h2),
.message.assistant .message-text :deep(h3),
.message.assistant .message-text :deep(h4),
.message.assistant .message-text :deep(h5),
.message.assistant .message-text :deep(h6) {
  margin: 16px 0 8px;
  font-weight: 600;
  line-height: 1.4;
  color: #4A5F7F;
}

.message.assistant .message-text :deep(h1) {
  font-size: 24px;
  border-bottom: 2px solid #D4DDFD;
  padding-bottom: 8px;
}

.message.assistant .message-text :deep(h2) {
  font-size: 20px;
  border-bottom: 1px solid #E8EFFF;
  padding-bottom: 6px;
}

.message.assistant .message-text :deep(h3) {
  font-size: 18px;
}

.message.assistant .message-text :deep(h4),
.message.assistant .message-text :deep(h5),
.message.assistant .message-text :deep(h6) {
  font-size: 16px;
}

.message.assistant .message-text :deep(ul),
.message.assistant .message-text :deep(ol) {
  padding-left: 24px;
  margin: 8px 0;
}

.message.assistant .message-text :deep(li) {
  margin: 6px 0;
  line-height: 1.7;
}

.message.assistant .message-text :deep(li > ul),
.message.assistant .message-text :deep(li > ol) {
  margin: 4px 0;
}

.message.assistant .message-text :deep(code) {
  background: rgba(90, 121, 214, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 14px;
  color: #5A7BD6;
}

.message.assistant .message-text :deep(pre) {
  background: #F5F7FA;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 12px 0;
  border: 1px solid #E8EFFF;
}

.message.assistant .message-text :deep(pre code) {
  background: transparent;
  padding: 0;
  color: #4A5F7F;
}

.message.assistant .message-text :deep(blockquote) {
  border-left: 4px solid #A6BDFB;
  padding-left: 16px;
  margin: 12px 0;
  color: #6A7B8A;
  background: rgba(166, 189, 251, 0.05);
  padding: 12px 16px;
  border-radius: 4px;
}

.message.assistant .message-text :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
}

.message.assistant .message-text :deep(th),
.message.assistant .message-text :deep(td) {
  border: 1px solid #D4DDFD;
  padding: 10px 14px;
  text-align: left;
}

.message.assistant .message-text :deep(th) {
  background: #F5F8FF;
  font-weight: 600;
  color: #4A5F7F;
}

.message.assistant .message-text :deep(tr:nth-child(even)) {
  background: #FAFBFF;
}

.message.assistant .message-text :deep(a) {
  color: #5A7BD6;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s ease;
}

.message.assistant .message-text :deep(a:hover) {
  border-bottom-color: #5A7BD6;
}

.message.assistant .message-text :deep(hr) {
  border: none;
  border-top: 1px solid #E8EFFF;
  margin: 16px 0;
}

.message.assistant .message-text :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 8px 0;
}

.message.assistant .message-text :deep(strong) {
  font-weight: 600;
  color: #4A5F7F;
}

.message.assistant .message-text :deep(em) {
  font-style: italic;
}

/* 输入区域 */
.input-area {
  padding: 20px 24px;
  border-top: 1px solid #E8F4F8;
  flex-shrink: 0;
}

.input-container {
  max-width: 900px;
  margin: 0 auto;
  background: #F5F8FF;
  border: 2px solid #D4DDFD;
  border-radius: 16px;
  padding: 12px 16px;
  transition: all 0.3s ease;
  width: 100%;
}

.input-container:focus-within {
  border-color: #A6BDFB;
  background: #FFFFFF;
  box-shadow: 0 4px 12px rgba(166, 189, 251, 0.2);
}

textarea {
  width: 100%;
  border: none;
  background: transparent;
  resize: none;
  font-size: 15px;
  color: #5A6B8A;
  outline: none;
  font-family: inherit;
  max-height: 200px;
}

textarea::placeholder {
  color: #A6BDFB;
  opacity: 0.6;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
}

.input-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8A9A9A;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.input-btn:hover {
  background: #E8F4F8;
  color: #5BA3C9;
}

.input-btn svg {
  width: 20px;
  height: 20px;
}

/* 发送按钮 */
.send-btn {
  height: 40px;
  border: none;
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  border-radius: 50%;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(166, 189, 251, 0.35);
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(166, 189, 251, 0.45);
  background: linear-gradient(135deg, #8FA8F5 0%, #7896F0 100%);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-btn svg {
  width: 20px;
  height: 20px;
}

.input-hint {
  text-align: center;
  font-size: 12px;
  color: #A6BDFB;
  margin-top: 12px;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(91, 163, 201, 0.5);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(91, 163, 201, 0.7);
}

/* 移动端遮罩 */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  animation: fadeIn 0.3s ease;
}

/* 知识库模式下移动端隐藏侧边栏 */
@media (max-width: 768px) {
  .sidebar.sidebar-hidden {
    display: none;
  }
}

/* 自定义提示框 */
.toast {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  background: #FFFFFF;
  padding: 14px 24px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 300px;
  max-width: 500px;
  z-index: 10000;
  border: 1px solid #E8EFFF;
}

.toast.success {
  border-left: 4px solid #10B981;
}

.toast.error {
  border-left: 4px solid #EF4444;
}

.toast-icon {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
}

.toast-icon svg {
  width: 100%;
  height: 100%;
}

.toast.success .toast-icon {
  color: #10B981;
}

.toast.error .toast-icon {
  color: #EF4444;
}

.toast-message {
  flex: 1;
  font-size: 14px;
  color: #4A5568;
  line-height: 1.5;
}

/* 提示框动画 */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(-50%) translateY(-20px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-20px);
}

/* 文件上传 Toast 提示 - 非阻塞式 */
.upload-toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1000;
  animation: slideInRight 0.3s ease;
}

.upload-toast-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(90, 106, 138, 0.25);
  min-width: 320px;
  max-width: 400px;
  border-left: 4px solid #A6BDFB;
}

.upload-toast.success .upload-toast-content {
  border-left-color: #6BCB77;
}

.upload-toast.error .upload-toast-content {
  border-left-color: #FF6B6B;
}

.upload-toast-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.upload-toast-icon .spinner {
  width: 28px;
  height: 28px;
  color: #A6BDFB;
  animation: rotate 1s linear infinite;
}

.upload-toast-icon .success-icon {
  width: 28px;
  height: 28px;
  color: #6BCB77;
}

.upload-toast-icon .error-icon {
  width: 28px;
  height: 28px;
  color: #FF6B6B;
}

.upload-toast-info {
  flex: 1;
  min-width: 0;
}

.upload-toast-filename {
  font-size: 14px;
  font-weight: 600;
  color: #5A6B8A;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.upload-toast-status {
  font-size: 12px;
  color: #8A9FD8;
  margin: 0 0 8px 0;
}

.upload-progress-bar {
  height: 4px;
  background: #E8EFFF;
  border-radius: 2px;
  overflow: hidden;
}

.upload-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #A6BDFB 0%, #8FA8F5 100%);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.upload-toast.success .upload-progress-fill {
  background: linear-gradient(90deg, #6BCB77 0%, #5CB85C 100%);
}

.upload-toast.error .upload-progress-fill {
  background: linear-gradient(90deg, #FF6B6B 0%, #FF5252 100%);
}

.upload-cancel-btn,
.upload-close-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.upload-cancel-btn {
  color: #8A9FD8;
}

.upload-cancel-btn:hover {
  background: #FFF0F0;
  color: #FF6B6B;
}

.upload-close-btn {
  color: #8A9FD8;
}

.upload-close-btn:hover {
  background: #F5F8FF;
  color: #5A7BD6;
}

.upload-cancel-btn svg,
.upload-close-btn svg {
  width: 16px;
  height: 16px;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .upload-toast {
    bottom: 16px;
    right: 16px;
    left: 16px;
  }
  
  .upload-toast-content {
    min-width: auto;
    max-width: none;
    width: 100%;
  }
}

/* 认证错误弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.3s ease;
}

.modal-container {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 0;
  max-width: 420px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  animation: slideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-header {
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  background: linear-gradient(135deg, #FEF2F2 0%, #FFE5E5 100%);
  border-bottom: 1px solid #FECDD3;
}

.modal-icon {
  width: 48px;
  height: 48px;
  color: #EF4444;
}

.modal-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: #991B1B;
  margin: 0;
}

.modal-body {
  padding: 32px 24px;
  text-align: center;
}

.modal-body p {
  font-size: 15px;
  color: #4A5568;
  line-height: 1.6;
  margin: 0 0 12px 0;
}

.modal-hint {
  font-size: 14px;
  color: #A0AEC0;
  margin-top: 8px !important;
}

.modal-footer {
  padding: 16px 24px 24px;
  display: flex;
  justify-content: center;
  gap: 12px;
  background: #F7FAFC;
}

.modal-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 28px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.modal-btn svg {
  width: 20px;
  height: 20px;
}

.modal-btn.primary {
  background: linear-gradient(135deg, #A6BDFB 0%, #8FA8F5 100%);
  color: #FFFFFF;
}

.modal-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(166, 189, 251, 0.4);
  background: linear-gradient(135deg, #8FA8F5 0%, #7896F0 100%);
}

.modal-btn:active {
  transform: translateY(0);
}

/* 弹窗动画 */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9) translateY(20px);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .sidebar {
    width: 260px;
    min-width: 260px;
    max-width: 280px;
  }
  
  .message-content {
    max-width: 80%;
  }
  
  .messages-container {
    max-width: 680px;
  }
  
  .input-container {
    max-width: 800px;
  }
}

@media (max-width: 1024px) {
  .sidebar {
    width: 240px;
    min-width: 240px;
    max-width: 260px;
  }
  
  .chat-header {
    padding: 12px 16px;
  }
  
  .chat-content {
    padding: 16px;
  }
  
  .input-area {
    padding: 16px;
  }
  
  .message-content {
    max-width: 80%;
  }
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 1000;
    width: 85%;
    min-width: 85%;
    max-width: 320px;
    transform: translateX(-100%);
    box-shadow: 2px 0 20px rgba(0, 0, 0, 0.15);
  }
  
  .sidebar.show {
    transform: translateX(0);
  }
  
  .sidebar.collapsed {
    transform: translateX(-100%);
  }
  
  .chat-main {
    width: 100%;
  }
  
  .model-selector span {
    display: none;
  }
  
  .header-right .header-btn:nth-child(1),
  .header-right .header-btn:nth-child(2) {
    display: none;
  }
  
  .message-content {
    max-width: 85%;
  }
  
  .chat-header {
    padding: 12px 16px;
  }
  
  .chat-content {
    padding: 12px;
  }
  
  .input-area {
    padding: 12px;
  }
  
  .input-container {
    padding: 10px 12px;
  }
  
  textarea {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .sidebar {
    width: 100%;
    min-width: 100%;
  }
  
  .message-content {
    max-width: 90%;
  }
  
  .message-text {
    padding: 12px 16px;
    font-size: 14px;
  }
  
  .welcome-message h1 {
    font-size: 24px;
  }
  
  .welcome-message p {
    font-size: 14px;
  }
  
  .input-actions {
    gap: 8px;
  }
  
  .action-buttons {
    display: none;
  }
}

/* 平板横屏优化 */
@media (max-width: 896px) and (orientation: landscape) {
  .chat-content {
    padding: 16px;
  }
  
  .input-area {
    padding: 12px 16px;
  }
  
  .message-text {
    padding: 12px 16px;
  }
}

/* 确保移动端触摸友好 */
@media (hover: none) and (pointer: coarse) {
  .history-item {
    padding: 10px 12px;
  }
  
  .header-btn {
    min-width: 44px;
    min-height: 44px;
  }
  
  .send-btn {
    min-width: 48px;
    min-height: 48px;
  }
}

/* 删除确认弹窗 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(90, 107, 138, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
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

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
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

</style>
