'use client'
import { useState, useEffect } from 'react'
import ProductCard from '@/components/products/ProductCard'
import ProductFilters from '@/components/products/ProductFilters'
import { ProductCardSkeleton } from '@/components/common/LoadingSkeleton'
import { products, Product } from '@/data/products'

export default function ProductsPage() {
  const [displayProducts, setDisplayProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])
  const [priceRange, setPriceRange] = useState(400)
  const [sortBy, setSortBy] = useState('featured')

  const categories = ['Office Supplies', 'Paper Products', 'Ink & Toner', 'Technology', 'Office Furniture', 'Office Machines']
  const maxPrice = 400

  useEffect(() => {
    // Simulate API loading
    setTimeout(() => {
      setDisplayProducts(products)
      setLoading(false)
    }, 800)
  }, [])

  const handleCategoryChange = (category: string) => {
    setSelectedCategories(prev =>
      prev.includes(category)
        ? prev.filter(c => c !== category)
        : [...prev, category]
    )
  }

  const handleApplyFilters = () => {
    let filtered = [...products]

    // Filter by category
    if (selectedCategories.length > 0) {
      filtered = filtered.filter(product =>
        selectedCategories.includes(product.category)
      )
    }

    // Filter by price
    filtered = filtered.filter(product => product.price <= priceRange)

    // Sort products
    switch (sortBy) {
      case 'price-low':
        filtered.sort((a, b) => a.price - b.price)
        break
      case 'price-high':
        filtered.sort((a, b) => b.price - a.price)
        break
      case 'newest':
        filtered.reverse()
        break
      default:
        break
    }

    setDisplayProducts(filtered)
  }

  const handleClearFilters = () => {
    setSelectedCategories([])
    setPriceRange(maxPrice)
    setSortBy('featured')
    setDisplayProducts(products)
  }

  return (
    <div className="container mx-auto px-4 py-6 md:py-8">
      <div className="mb-6 md:mb-8">
        <h1 className="text-2xl md:text-4xl font-bold mb-2">All Products</h1>
        <p className="text-gray-600 text-sm md:text-base">Discover our complete range of office supplies</p>
      </div>
      
      <div className="flex flex-col md:flex-row gap-6 md:gap-8">
        {/* Smart Filters */}
        <ProductFilters
          categories={categories}
          selectedCategories={selectedCategories}
          priceRange={priceRange}
          maxPrice={maxPrice}
          onCategoryChange={handleCategoryChange}
          onPriceChange={setPriceRange}
          onApplyFilters={handleApplyFilters}
          onClearFilters={handleClearFilters}
        />

        {/* Products Grid */}
        <div className="flex-1">
          {/* Sort & Count Header */}
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 sm:gap-0 mb-6">
            <p className="text-gray-600 text-sm md:text-base">
              {loading ? 'Loading products...' : `${displayProducts.length} Products Found`}
            </p>
            <select
              value={sortBy}
              onChange={(e) => {
                setSortBy(e.target.value)
                handleApplyFilters()
              }}
              className="border px-3 md:px-4 py-2 rounded-lg text-sm md:text-base w-full sm:w-auto focus:outline-none focus:border-primary"
            >
              <option value="featured">Sort by: Featured</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
              <option value="newest">Newest First</option>
            </select>
          </div>

          {/* Products Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
            {loading ? (
              Array.from({ length: 6 }).map((_, i) => (
                <ProductCardSkeleton key={i} />
              ))
            ) : displayProducts.length > 0 ? (
              displayProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))
            ) : (
              <div className="col-span-2 lg:col-span-3 text-center py-16">
                <div className="text-gray-400 mb-4">
                  <svg className="w-24 h-24 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">No Products Found</h3>
                <p className="text-gray-500 mb-4">Try adjusting your filters</p>
                <button
                  onClick={handleClearFilters}
                  className="bg-primary text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
                >
                  Clear Filters
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}