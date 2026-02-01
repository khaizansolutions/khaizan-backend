'use client'
import { useState, useEffect, useRef } from 'react'
import { Search, X, TrendingUp } from 'lucide-react'
import Link from 'next/link'
import Image from 'next/image'
import { products, Product } from '@/data/products'

interface SmartSearchProps {
  onClose?: () => void
}

export default function SmartSearch({ onClose }: SmartSearchProps) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Product[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const [recentSearches, setRecentSearches] = useState<string[]>([])
  const searchRef = useRef<HTMLDivElement>(null)

  // Popular searches
  const popularSearches = [
    'Office Chair',
    'Printer Paper',
    'Desk Organizer',
    'Wireless Mouse',
    'Stapler',
  ]

  // Load recent searches from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('recentSearches')
    if (saved) {
      setRecentSearches(JSON.parse(saved))
    }
  }, [])

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Smart search algorithm
  const handleSearch = (searchQuery: string) => {
    setQuery(searchQuery)
    
    if (searchQuery.trim().length < 2) {
      setResults([])
      setIsOpen(false)
      return
    }

    const lowerQuery = searchQuery.toLowerCase()
    
    // Search in name, category, brand, and description
    const filteredProducts = products.filter(product => 
      product.name.toLowerCase().includes(lowerQuery) ||
      product.category.toLowerCase().includes(lowerQuery) ||
      product.brand.toLowerCase().includes(lowerQuery) ||
      product.description.toLowerCase().includes(lowerQuery) ||
      product.sku.toLowerCase().includes(lowerQuery)
    )

    // Sort by relevance (exact match first, then partial)
    const sorted = filteredProducts.sort((a, b) => {
      const aExact = a.name.toLowerCase().startsWith(lowerQuery)
      const bExact = b.name.toLowerCase().startsWith(lowerQuery)
      if (aExact && !bExact) return -1
      if (!aExact && bExact) return 1
      return 0
    })

    setResults(sorted.slice(0, 8)) // Show top 8 results
    setIsOpen(true)
  }

  // Save search to recent searches
  const saveSearch = (searchTerm: string) => {
    const updated = [searchTerm, ...recentSearches.filter(s => s !== searchTerm)].slice(0, 5)
    setRecentSearches(updated)
    localStorage.setItem('recentSearches', JSON.stringify(updated))
  }

  const handleProductClick = (productName: string) => {
    saveSearch(productName)
    setIsOpen(false)
    setQuery('')
    onClose?.()
  }

  const handleQuickSearch = (searchTerm: string) => {
    setQuery(searchTerm)
    handleSearch(searchTerm)
    saveSearch(searchTerm)
  }

  const clearSearch = () => {
    setQuery('')
    setResults([])
    setIsOpen(false)
  }

  const clearRecentSearches = () => {
    setRecentSearches([])
    localStorage.removeItem('recentSearches')
  }

  return (
    <div ref={searchRef} className="relative w-full">
      {/* Search Input */}
      <div className="relative">
        <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
          <Search size={20} />
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
          onFocus={() => query.length >= 2 && setIsOpen(true)}
          placeholder="Search for products, brands, categories..."
          className="w-full pl-10 pr-10 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary transition"
        />
        {query && (
          <button
            onClick={clearSearch}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
          >
            <X size={20} />
          </button>
        )}
      </div>

      {/* Search Dropdown */}
      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-lg shadow-2xl border border-gray-200 max-h-[600px] overflow-y-auto z-50">
          {/* Results Section */}
          {results.length > 0 ? (
            <div className="p-4">
              <div className="flex justify-between items-center mb-3">
                <h3 className="font-semibold text-gray-700">Search Results ({results.length})</h3>
                <Link 
                  href={`/products?search=${encodeURIComponent(query)}`}
                  className="text-sm text-primary hover:underline"
                  onClick={() => {
                    saveSearch(query)
                    setIsOpen(false)
                    onClose?.()
                  }}
                >
                  View All
                </Link>
              </div>
              
              <div className="space-y-2">
                {results.map((product) => (
                  <Link
                    key={product.id}
                    href={`/products/${product.id}`}
                    onClick={() => handleProductClick(product.name)}
                    className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg transition group"
                  >
                    <div className="relative w-16 h-16 flex-shrink-0 bg-gray-100 rounded">
                      <Image
                        src={product.image}
                        alt={product.name}
                        fill
                        className="object-cover rounded"
                      />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-gray-900 group-hover:text-primary truncate">
                        {product.name}
                      </h4>
                      <p className="text-sm text-gray-500">{product.category}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-primary">AED {product.price.toFixed(2)}</p>
                      {product.originalPrice && (
                        <p className="text-xs text-gray-400 line-through">
                          AED {product.originalPrice.toFixed(2)}
                        </p>
                      )}
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          ) : query.length >= 2 ? (
            // No results found
            <div className="p-8 text-center">
              <div className="text-gray-400 mb-3">
                <Search size={48} className="mx-auto" />
              </div>
              <h3 className="font-semibold text-gray-700 mb-1">No products found</h3>
              <p className="text-sm text-gray-500">Try searching with different keywords</p>
            </div>
          ) : null}

          {/* Suggestions when search is empty or < 2 chars */}
          {query.length < 2 && (
            <div className="p-4 border-t">
              {/* Recent Searches */}
              {recentSearches.length > 0 && (
                <div className="mb-6">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="font-semibold text-gray-700 text-sm">Recent Searches</h3>
                    <button
                      onClick={clearRecentSearches}
                      className="text-xs text-gray-500 hover:text-gray-700"
                    >
                      Clear
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {recentSearches.map((search, index) => (
                      <button
                        key={index}
                        onClick={() => handleQuickSearch(search)}
                        className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm transition"
                      >
                        {search}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Popular Searches */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <TrendingUp size={16} className="text-primary" />
                  <h3 className="font-semibold text-gray-700 text-sm">Popular Searches</h3>
                </div>
                <div className="flex flex-wrap gap-2">
                  {popularSearches.map((search, index) => (
                    <button
                      key={index}
                      onClick={() => handleQuickSearch(search)}
                      className="px-3 py-1 bg-blue-50 hover:bg-blue-100 text-primary rounded-full text-sm transition"
                    >
                      {search}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}