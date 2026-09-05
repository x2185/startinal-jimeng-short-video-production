import { useEffect, useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import './App.css'

type User = { id: number; email: string; display_name: string; role: 'admin' | 'user' }
type Product = {
  id: number
  name: string
  shop_url?: string | null
  target_market?: string
  language?: string
  selling_points: string
  restrictions: string
  asset_root: string
  status: string
  created_at?: string
  updated_at?: string
}
type Package = {
  package_id: number
  product_name: string
  creative_route: string
  output_path: string
  status: string
  reviewer_note?: string
  requester_name: string
  script?: string
  storyboard?: string
  prompt_notes?: string
}
type Asset = { asset_id: number; source_path: string; media_type: string; category: string; bytes: number; created_at: string }

const API = import.meta.env.VITE_API_URL ?? '/api'

async function api<T>(path: string, token = '', options: RequestInit = {}) {
  const response = await fetch(API + path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })
  const raw = await response.text()
  const body = raw
    ? (() => {
        try {
          return JSON.parse(raw)
        } catch {
          return { detail: raw }
        }
      })()
    : {}
  if (!response.ok) throw new Error(body.detail || '请求失败')
  return body as T
}

function App() {
  const [token, setToken] = useState(localStorage.getItem('production-hub-token') ?? '')
  const [user, setUser] = useState<User | null>(null)
  const [bootstrap, setBootstrap] = useState<boolean | null>(null)
  const [products, setProducts] = useState<Product[]>([])
  const [packages, setPackages] = useState<Package[]>([])
  const [notice, setNotice] = useState('')
  const [catalogRoot, setCatalogRoot] = useState('')
  const [catalogSummary, setCatalogSummary] = useState('')
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null)
  const [selectedAssets, setSelectedAssets] = useState<Asset[]>([])
  const [selectedPackage, setSelectedPackage] = useState<Package | null>(null)

  const load = async (activeToken = token) => {
    const [me, ps, packs] = await Promise.all([
      api<User>('/me', activeToken),
      api<Product[]>('/products', activeToken),
      api<Package[]>('/packages', activeToken),
    ])
    setUser(me)
    setProducts(ps)
    setPackages(packs)
  }

  useEffect(() => {
    api<{ needs_bootstrap: boolean }>('/setup-status')
      .then((x) => setBootstrap(x.needs_bootstrap))
      .catch(() => setNotice('无法连接后端，请确认后端服务正在运行。'))
    if (token) load().catch(() => logout())
  }, [token])

  const logout = () => {
    localStorage.removeItem('production-hub-token')
    setToken('')
    setUser(null)
  }

  const signIn = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const data = Object.fromEntries(new FormData(event.currentTarget))
    try {
      const result = await api<{ token: string; user: User }>(bootstrap ? '/bootstrap' : '/login', '', {
        method: 'POST',
        body: JSON.stringify(data),
      })
      localStorage.setItem('production-hub-token', result.token)
      setToken(result.token)
      setUser(result.user)
      setBootstrap(false)
      await load(result.token)
    } catch (error) {
      setNotice(error instanceof Error ? error.message : '登录失败')
    }
  }

  const addProduct = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    try {
      await api('/products', token, {
        method: 'POST',
        body: JSON.stringify(Object.fromEntries(new FormData(event.currentTarget))),
      })
      event.currentTarget.reset()
      setNotice('商品档案已创建。')
      await load()
    } catch (error) {
      setNotice(error instanceof Error ? error.message : '创建商品失败')
    }
  }

  const makePackage = async (product: Product, kind: 'ugc_mix' | 'product_showcase') => {
    try {
      const created = await api<Package>('/packages', token, {
        method: 'POST',
        body: JSON.stringify({
          product_id: product.id,
          content_type: kind,
          creative_route: kind === 'ugc_mix' ? '真实开箱 + 功能证明' : '细节优先商品展示',
        }),
      })
      setNotice(`任务已创建，输出路径：${created.output_path}`)
      await load()
    } catch (error) {
      setNotice(error instanceof Error ? error.message : '生成生产包失败')
    }
  }

  const submitTask = async (packageId: number) => {
    try {
      await api(`/packages/${packageId}/submit`, token, { method: 'POST' })
      setNotice('任务已提交。')
      await load()
    } catch (error) {
      setNotice(error instanceof Error ? error.message : '提交任务失败')
    }
  }

  const completeTask = async (packageId: number) => {
    try {
      await api(`/packages/${packageId}/complete`, token, { method: 'POST' })
      setNotice('任务已标记为成片。')
      await load()
    } catch (error) {
      setNotice(error instanceof Error ? error.message : '标记成片失败')
    }
  }

  const regenerateTask = async (packageId: number) => {
    try {
      const updated = await api<Package>(`/packages/${packageId}/regenerate`, token, { method: 'POST' })
      setPackages((current) => current.map((item) => (item.package_id === packageId ? updated : item)))
      setSelectedPackage(updated)
      setNotice('提示词已重新生成。')
    } catch (error) {
      setNotice(error instanceof Error ? error.message : '重新生成提示词失败')
    }
  }

  const deleteTask = async (packageId: number) => {
    try {
      await api(`/packages/${packageId}`, token, { method: 'DELETE' })
      setPackages((current) => current.filter((item) => item.package_id !== packageId))
      setNotice('任务已删除。')
      return true
    } catch (error) {
      setNotice(error instanceof Error ? error.message : '删除任务失败')
      return false
    }
  }

  const copyPath = async (path: string) => {
    try {
      await navigator.clipboard.writeText(path)
      setNotice('输出路径已复制。')
    } catch {
      setNotice(path)
    }
  }

  const scanAssets = async (product: Product) => {
    if (!product.asset_root) {
      setNotice('请先在商品档案中填写本地素材文件夹路径。')
      return
    }
    try {
      const result = await api<{ indexed: number; duplicates: number; ignored: number; by_type: Record<string, number> }>(
        '/products/' + product.id + '/scan',
        token,
        { method: 'POST', body: JSON.stringify({ source_path: product.asset_root }) },
      )
      setNotice(`素材扫描完成：新增 ${result.indexed} 个，重复 ${result.duplicates} 个，忽略 ${result.ignored} 个。`)
      await load()
    } catch (error) {
      setNotice(error instanceof Error ? error.message : '扫描素材失败')
    }
  }

  const updateProduct = async (productId: number, payload: Omit<Product, 'id' | 'status'>) => {
    try {
      const updated = await api<Product>(`/products/${productId}`, token, {
        method: 'PATCH',
        body: JSON.stringify(payload),
      })
      setSelectedProduct(updated)
      setNotice('商品档案已更新。')
      await load()
      return updated
    } catch (error) {
      setNotice(error instanceof Error ? error.message : '更新商品失败')
      throw error
    }
  }

  const uploadCatalog = async (files: FileList) => {
    const form = new FormData()
    const relativeNames = Array.from(files).map((file) => (file as File & { webkitRelativePath?: string }).webkitRelativePath || file.name)
    const topLevelFolders = new Set(relativeNames.map((name) => name.split(/[\\/]/)[0]).filter(Boolean))
    Array.from(files).forEach((file, index) =>
      form.append('files', file, relativeNames[index]),
    )
    try {
      const response = await fetch(API + '/catalog/upload', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: form,
      })
      const raw = await response.text()
      const body = raw
        ? (() => {
            try {
              return JSON.parse(raw)
            } catch {
              return { detail: raw }
            }
          })()
        : {}
      if (!response.ok) throw new Error(body.detail || '文件夹导入失败')
      const folderLabel = topLevelFolders.size === 1 ? [...topLevelFolders][0] : `${topLevelFolders.size} 个产品文件夹`
      const catalogLabel = folderLabel ? `${folderLabel} · ${files.length} 个文件` : `${files.length} 个文件`
      setCatalogRoot(catalogLabel)
      setCatalogSummary(`新建商品 ${body.products_created} 个，新增素材 ${body.assets_indexed} 个。`)
      setNotice('文件夹导入完成。')
      await load()
    } catch (error) {
      setCatalogSummary('')
      setNotice(error instanceof Error ? error.message : '文件夹导入失败')
    }
  }

  const openProduct = async (product: Product) => {
    setSelectedProduct(product)
    try {
      setSelectedAssets(await api<Asset[]>('/products/' + product.id + '/assets', token))
    } catch {
      setSelectedAssets([])
    }
  }

  if (bootstrap === null) return <main className="loading">正在打开 Startinal 商品视频工坊…</main>
  if (!user) {
    return (
      <main className="auth-shell">
        <section className="auth-copy">
          <p className="eyebrow">Startinal 商品视频工坊</p>
          <h1>从商品资料，生成可直接生产的 TikTok 内容包。</h1>
          <p>素材本地保存，流程统一管理；API 密钥仅由管理员保管。</p>
          <div className="steps">
            <span>01 产品资料</span>
            <span>02 脚本与分镜</span>
            <span>03 生成与导出</span>
          </div>
        </section>
        <form className="auth-card" onSubmit={signIn}>
          <p className="eyebrow">{bootstrap ? '首次设置' : '欢迎回来'}</p>
          <h2>{bootstrap ? '创建管理员账号' : '登录工作台'}</h2>
          {bootstrap && (
            <label>
              姓名
              <input name="display_name" defaultValue="管理员" required />
            </label>
          )}
          <label>
            账号
            <input type="text" name="email" defaultValue={bootstrap ? 'admin' : undefined} required />
          </label>
          <label>
            密码
            <input type="password" name="password" defaultValue={bootstrap ? 'admin' : undefined} minLength={4} required />
          </label>
          <button type="submit">{bootstrap ? '创建工作区' : '登录'}</button>
          {notice && <p className="notice">{notice}</p>}
        </form>
      </main>
    )
  }

  return (
    <main className="app-shell">
      <aside>
        <div className="brand">
          <b className="brand-mark" aria-label="Startinal 商品视频工坊">
            <svg viewBox="0 0 40 40" aria-hidden="true">
              <path d="M9 8.5h14.8A5.2 5.2 0 0 1 29 13.7v12.6a5.2 5.2 0 0 1-5.2 5.2H9A5.2 5.2 0 0 1 3.8 26.3V13.7A5.2 5.2 0 0 1 9 8.5Z" fill="none" stroke="currentColor" strokeWidth="2.4" />
              <path d="m29 16 7-4.2v16.4L29 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinejoin="round" />
              <path d="m15 15 7 5-7 5v-10Z" fill="currentColor" />
            </svg>
          </b>
          <div>
            <strong>Startinal Product Motion Forge</strong>
            <small>本地素材工作流</small>
          </div>
        </div>
        <nav>
          <button type="button" className="active">工作区</button>
        </nav>
        <div className="profile">
          <strong>{user.display_name}</strong>
          <small>{user.role === 'admin' ? '开发者 / 管理员' : '普通用户'}</small>
          <button type="button" onClick={logout}>退出登录</button>
        </div>
      </aside>
      <section className="content">
        <header>
          <div>
            <p className="eyebrow">内容工作区</p>
            <h1>让下一个商品更快进入生产。</h1>
          </div>
          <span className="mode">● 本地素材模式</span>
        </header>
        {notice && <p className="notice banner">{notice}</p>}
        <Workspace
          products={products}
          packages={packages}
          addProduct={addProduct}
          makePackage={makePackage}
          submitTask={submitTask}
          completeTask={completeTask}
          deleteTask={deleteTask}
          copyPath={copyPath}
          scanAssets={scanAssets}
          updateProduct={updateProduct}
          uploadCatalog={uploadCatalog}
          catalogRoot={catalogRoot}
          catalogSummary={catalogSummary}
          selectedProduct={selectedProduct}
          selectedAssets={selectedAssets}
          selectedPackage={selectedPackage}
          openProduct={openProduct}
          closeProduct={() => setSelectedProduct(null)}
          openPackage={(item) => setSelectedPackage(item)}
          closePackage={() => setSelectedPackage(null)}
          regeneratePackage={regenerateTask}
        />
      </section>
    </main>
  )
}

function Workspace({
  products,
  packages,
  addProduct,
  makePackage,
  submitTask,
  completeTask,
  deleteTask,
  copyPath,
  scanAssets,
  updateProduct,
  uploadCatalog,
  catalogRoot,
  catalogSummary,
  selectedProduct,
  selectedAssets,
  selectedPackage,
  openProduct,
  closeProduct,
  openPackage,
  closePackage,
  regeneratePackage,
}: {
  products: Product[]
  packages: Package[]
  addProduct: (e: FormEvent<HTMLFormElement>) => void
  makePackage: (p: Product, k: 'ugc_mix' | 'product_showcase') => void
  submitTask: (packageId: number) => void
  completeTask: (packageId: number) => void
  deleteTask: (packageId: number) => Promise<boolean>
  copyPath: (path: string) => void
  scanAssets: (p: Product) => void
  updateProduct: (productId: number, payload: Omit<Product, 'id' | 'status'>) => Promise<Product>
  uploadCatalog: (files: FileList) => void
  catalogRoot: string
  catalogSummary: string
  selectedProduct: Product | null
  selectedAssets: Asset[]
  selectedPackage: Package | null
  openProduct: (p: Product) => void
  closeProduct: () => void
  openPackage: (p: Package) => void
  closePackage: () => void
  regeneratePackage: (packageId: number) => void
  }) {
  const [productQuery, setProductQuery] = useState('')
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null)
  const [deletingId, setDeletingId] = useState<number | null>(null)
  const [productDraft, setProductDraft] = useState<Omit<Product, 'id' | 'status'> | null>(null)

  useEffect(() => {
    if (!selectedProduct) {
      setProductDraft(null)
      return
    }
    setProductDraft({
      name: selectedProduct.name,
      shop_url: selectedProduct.shop_url ?? '',
      target_market: selectedProduct.target_market ?? 'United States',
      language: selectedProduct.language ?? 'English (US)',
      selling_points: selectedProduct.selling_points ?? '',
      restrictions: selectedProduct.restrictions ?? '',
      asset_root: selectedProduct.asset_root ?? '',
    })
  }, [selectedProduct])

  const filteredProducts = useMemo(
    () => products.filter((product) => product.name.toLowerCase().includes(productQuery.trim().toLowerCase())),
    [products, productQuery],
  )

  const draftTasks = packages.filter((item) => item.status === 'draft' || item.status === 'changes_requested')
  const processingTasks = packages.filter((item) => item.status === 'submitted')
  const doneTasks = packages.filter((item) => item.status === 'approved')

  const renderTask = (item: Package) => {
    const editable = item.status === 'draft' || item.status === 'changes_requested'
      const processing = item.status === 'submitted'
      const done = item.status === 'approved'
      const deleting = pendingDeleteId === item.package_id
      const busyDeleting = deletingId === item.package_id
      return (
        <article className="task-row" key={item.package_id}>
        <div className="task-main">
          <strong>{item.product_name}</strong>
          <span>{item.creative_route}</span>
          <small>{item.output_path || '输出路径待生成'}</small>
        </div>
        <div className="task-actions">
          {editable && <button type="button" className="secondary" onClick={() => submitTask(item.package_id)}>确认提交</button>}
          {processing && <button type="button" className="secondary" onClick={() => completeTask(item.package_id)}>标记成片</button>}
          {done && (
            <>
              <button type="button" className="secondary" onClick={() => openPackage(item)}>查看提示词</button>
              {item.output_path && <button type="button" className="secondary" onClick={() => copyPath(item.output_path)}>复制路径</button>}
            </>
          )}
            {deleting ? (
              <>
                <button
                  type="button"
                  className="secondary danger"
                  disabled={busyDeleting}
                  onClick={async () => {
                    setDeletingId(item.package_id)
                    try {
                      const deleted = await deleteTask(item.package_id)
                      if (deleted) setPendingDeleteId(null)
                    } finally {
                      setDeletingId((current) => (current === item.package_id ? null : current))
                    }
                  }}
                >
                  {busyDeleting ? '删除中…' : '确认删除'}
                </button>
                <button type="button" className="secondary" onClick={() => setPendingDeleteId(null)} disabled={busyDeleting}>
                  取消
                </button>
              </>
            ) : (
              <button type="button" className="secondary danger" onClick={() => setPendingDeleteId(item.package_id)}>删除</button>
            )}
        </div>
      </article>
    )
  }

  return (
    <>
      <section className="summary">
        <article>
          <strong>{products.length}</strong>
          <span>商品档案</span>
        </article>
        <article>
          <strong>{packages.length}</strong>
          <span>内容任务</span>
        </article>
        <article>
          <strong>{selectedProduct ? selectedAssets.length : '—'}</strong>
          <span>{selectedProduct ? '当前素材数' : '点击商品查看详情'}</span>
        </article>
      </section>

      {selectedProduct && (
        <section className="panel product-detail">
          <div className="detail-head">
            <div>
              <p className="eyebrow">商品档案详情</p>
              <h2>{selectedProduct.name}</h2>
            </div>
            <button type="button" className="secondary" onClick={closeProduct}>关闭详情</button>
          </div>
          <form
            className="product-edit-form"
            onSubmit={async (event) => {
              event.preventDefault()
              if (!selectedProduct || !productDraft) return
              await updateProduct(selectedProduct.id, productDraft)
            }}
          >
            <div className="product-edit-grid">
              <label>
                商品名称
                <input
                  value={productDraft?.name ?? ''}
                  onChange={(event) => setProductDraft((current) => current ? { ...current, name: event.target.value } : current)}
                  required
                />
              </label>
              <label>
                商品链接
                <input
                  value={productDraft?.shop_url ?? ''}
                  onChange={(event) => setProductDraft((current) => current ? { ...current, shop_url: event.target.value } : current)}
                  placeholder="可留空"
                />
              </label>
              <label>
                市场
                <input
                  value={productDraft?.target_market ?? ''}
                  onChange={(event) => setProductDraft((current) => current ? { ...current, target_market: event.target.value } : current)}
                />
              </label>
              <label>
                语言
                <input
                  value={productDraft?.language ?? ''}
                  onChange={(event) => setProductDraft((current) => current ? { ...current, language: event.target.value } : current)}
                />
              </label>
            </div>
            <label>
              素材目录
              <input
                value={productDraft?.asset_root ?? ''}
                onChange={(event) => setProductDraft((current) => current ? { ...current, asset_root: event.target.value } : current)}
                placeholder="本地文件夹路径"
              />
            </label>
            <label>
              已确认卖点
              <textarea
                value={productDraft?.selling_points ?? ''}
                onChange={(event) => setProductDraft((current) => current ? { ...current, selling_points: event.target.value } : current)}
                placeholder="每行一个，只写能证明的事实"
              />
            </label>
            <label>
              限制内容
              <textarea
                value={productDraft?.restrictions ?? ''}
                onChange={(event) => setProductDraft((current) => current ? { ...current, restrictions: event.target.value } : current)}
                placeholder="不能使用的功效、画面、声明或要求"
              />
            </label>
            <div className="detail-actions">
              <button type="submit">保存修改</button>
              <button type="button" className="secondary" onClick={() => scanAssets(selectedProduct)}>
                重新扫描
              </button>
            </div>
          </form>
          <h3>已扫描素材（{selectedAssets.length}）</h3>
          {selectedAssets.length === 0 ? (
            <p className="muted">尚未扫描素材，或当前文件夹为空。</p>
          ) : (
            <div className="asset-list">
              {selectedAssets.map((asset) => (
                <div key={asset.asset_id}>
                  <span>{asset.category} · {asset.media_type}</span>
                  <small>{asset.source_path}</small>
                </div>
              ))}
            </div>
          )}
        </section>
      )}

      <section className="panel bulk-import">
        <p className="eyebrow">批量导入</p>
        <h2>点击选择产品总文件夹。</h2>
        <p className="muted">按第一层子文件夹自动创建商品档案，并扫描每个产品的图片、视频和文档。</p>
        {catalogRoot && (
          <p className="bulk-status" role="status" aria-live="polite">
            <strong>{catalogRoot}</strong>
            {catalogSummary && <span>{catalogSummary}</span>}
          </p>
        )}
        <div className="bulk-row">
          <input
            id="catalog-folder-picker"
            type="file"
            {...({ webkitdirectory: 'true', directory: '' } as Record<string, string>)}
            onChange={(event) => {
              if (event.target.files?.length) uploadCatalog(event.target.files)
              event.currentTarget.value = ''
            }}
          />
          <input
            className="folder-path-input"
            value={catalogRoot}
            readOnly
            onClick={() => document.getElementById('catalog-folder-picker')?.click()}
            placeholder="点击选择产品总文件夹"
            title="点击选择产品总文件夹"
          />
        </div>
      </section>

      <section className="two-column">
        <form className="panel product-form" onSubmit={addProduct}>
          <p className="eyebrow">新建单个商品</p>
          <h2>先把事实整理清楚。</h2>
          <label>
            商品名称
            <input name="name" required placeholder="例如：磁力积木套装" />
          </label>
          <label>
            TikTok Shop 商品链接
            <input name="shop_url" placeholder="可暂时留空" />
          </label>
          <label>
            已确认的卖点
            <textarea name="selling_points" placeholder="每行一个，只填写能展示或验证的事实。" />
          </label>
          <label>
            本地素材文件夹
            <textarea name="asset_root" placeholder="D:\\Startinal商品视频工坊\\素材\\商品名称" />
          </label>
          <label>
            限制 / 禁用内容
            <textarea name="restrictions" placeholder="不能使用的功效、画面、声明或安全要求…" />
          </label>
          <button type="submit">创建商品档案</button>
        </form>

        <section className="panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">我的商品</p>
              <h2>生成内容任务。</h2>
            </div>
            <input
              className="search-input"
              value={productQuery}
              onChange={(event) => setProductQuery(event.target.value)}
              placeholder="搜索商品名称"
            />
          </div>
          <div className="product-list">
            {products.length === 0 && <p className="muted">先创建一个商品档案，或使用上方批量导入。</p>}
            {products.length > 0 && filteredProducts.length === 0 && <p className="muted">没有匹配的商品。</p>}
            {filteredProducts.map((product) => (
              <article className="product-card" key={product.id} onClick={() => openProduct(product)}>
                <div>
                  <h3>{product.name}</h3>
                  <small>{product.asset_root || '尚未登记本地文件夹'}</small>
                  <button type="button" className="link-button" onClick={(event) => { event.stopPropagation(); openProduct(product) }}>
                    查看档案
                  </button>
                </div>
                <div className="actions">
                  <button type="button" className="secondary" onClick={(event) => { event.stopPropagation(); scanAssets(product) }}>补扫素材</button>
                  <button type="button" className="secondary" onClick={(event) => { event.stopPropagation(); makePackage(product, 'ugc_mix') }}>口播混剪</button>
                  <button type="button" className="secondary" onClick={(event) => { event.stopPropagation(); makePackage(product, 'product_showcase') }}>商品展示</button>
                </div>
              </article>
            ))}
          </div>
        </section>
      </section>

      <section className="panel task-board">
        <div className="section-heading">
          <div>
            <p className="eyebrow">任务看板</p>
            <h2>只保留确认、处理和成片。</h2>
          </div>
          <div className="task-chips">
            <span>草稿 {draftTasks.length}</span>
            <span>处理中 {processingTasks.length}</span>
            <span>已完成 {doneTasks.length}</span>
          </div>
        </div>
        <p className="muted">草稿先确认提交；处理中等待成片；完成后只看输出路径。</p>

        {selectedPackage && (
          <section className="package-detail">
            <div className="section-heading">
              <div>
                <p className="eyebrow">任务详情</p>
                <h3>{selectedPackage.product_name}</h3>
              </div>
              <button type="button" className="secondary" onClick={closePackage}>关闭详情</button>
            </div>
            <p><strong>创意方向：</strong>{selectedPackage.creative_route}</p>
            <p><strong>输出路径：</strong>{selectedPackage.output_path || '待生成'}</p>
            <div className="detail-actions">
              <button type="button" onClick={() => regeneratePackage(selectedPackage.package_id)}>重新生成提示词</button>
              {selectedPackage.output_path && (
                <button type="button" className="secondary" onClick={() => copyPath(selectedPackage.output_path)}>复制路径</button>
              )}
            </div>
            <div className="package-text">
              <h4>脚本</h4>
              <pre>{selectedPackage.script || '暂无脚本内容。'}</pre>
            </div>
            <div className="package-text">
              <h4>分镜</h4>
              <pre>{selectedPackage.storyboard || '暂无分镜内容。'}</pre>
            </div>
            <div className="package-text">
              <h4>20 个提示词</h4>
              <pre>{selectedPackage.prompt_notes || '暂无提示词内容。'}</pre>
            </div>
          </section>
        )}

        <div className="task-groups">
          <section className="task-group">
            <h3>草稿和待调整</h3>
            {draftTasks.length === 0 ? <p className="muted">没有草稿任务。</p> : <div className="task-list">{draftTasks.map(renderTask)}</div>}
          </section>

          <section className="task-group">
            <h3>处理中</h3>
            {processingTasks.length === 0 ? <p className="muted">没有处理中任务。</p> : <div className="task-list">{processingTasks.map(renderTask)}</div>}
          </section>

          <section className="task-group">
            <h3>已完成</h3>
            {doneTasks.length === 0 ? <p className="muted">没有成片任务。</p> : <div className="task-list">{doneTasks.map(renderTask)}</div>}
          </section>
        </div>
      </section>
    </>
  )
}

export default App
