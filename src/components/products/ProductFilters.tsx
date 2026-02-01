'use client'
import { useState } from 'react'
import { ChevronDown, ChevronUp, X, SlidersHorizontal } from 'lucide-react'

interface ProductFiltersProps {
  categories: string[]
  selectedCategories: string[]
  priceRange: number
  maxPrice: number
  onCategoryChange: (category: string) => void
  onPriceChange: (price: number) => void
  onApplyFilters: () => void
  onClearFilters: () => void
}

export default function ProductFilters({
  categories,
  selectedCategories,
  priceRange,
  maxPrice,
  onCategoryChange,
  onPriceChange,
  onApplyFilters,
  onClearFilters,
}: ProductFiltersProps) {
  const [isCategoryOpen, setIsCategoryOpen] = useState(true)
  const [isPriceOpen, setIsPriceOpen] = useState(true)
  const [isMobileFilterOpen, setIsMobileFilterOpen] = useState(false)

  const hasActiveFilters = selectedCategories.length > 0 || priceRange < maxPrice

  return (
    <>
      {/* Mobile Filter Button */}
      <div className="md:hidden mb-4">
        <button
          onClick={() => setIsMobileFilterOpen(!isMobileFilterOpen)}
          className="w-full bg-white border-2 border-gray-300 rounded-lg px-4 py-3 flex items-center justify-between hover:border-primary transition"
        >
          <div className="flex items-center gap-2">
            <SlidersHorizontal size={20} />
            <span className="font-semibold">Filters</span>
            {hasActiveFilters && (
              <span className="bg-primary text-white text-xs px-2 py-0.5 rounded-full">
                {selectedCategories.length + (priceRange < maxPrice ? 1 : 0)}
              </span>
            )}
          </div>
          {isMobileFilterOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
      </div>

      {/* Filter Sidebar */}
      <aside
        className={`
          fixed md:static inset-0 z-50 md:z-auto
          ${isMobileFilterOpen ? 'block' : 'hidden md:block'}
          md:w-64 md:shrink-0
        `}
      >
        {/* Mobile Overlay */}
        {isMobileFilterOpen && (
          <div
            className="fixed inset-0 bg-black/50 md:hidden"
            onClick={() => setIsMobileFilterOpen(false)}
          />
        )}

        {/* Filter Panel */}
        <div
          className={`
            fixed md:static right-0 top-0 bottom-0 w-80 md:w-full
            bg-white md:rounded-lg shadow-xl md:shadow-md
            overflow-y-auto md:sticky md:top-24
            transform transition-transform duration-300
            ${isMobileFilterOpen ? 'translate-x-0' : 'translate-x-full md:translate-x-0'}
          `}
        >
          {/* Mobile Header */}
          <div className="md:hidden flex items-center justify-between p-4 border-b sticky top-0 bg-white z-10">
            <h3 className="font-bold text-lg">Filters</h3>
            <button onClick={() => setIsMobileFilterOpen(false)}>
              <X size={24} />
            </button>
          </div>

          <div className="p-4 md:p-6">
            {/* Desktop Header */}
            <div className="hidden md:flex justify-between items-center mb-4">
              <h3 className="font-bold text-lg">Filters</h3>
              {hasActiveFilters && (
                <button
                  onClick={onClearFilters}
                  className="text-sm text-primary hover:underline"
                >
                  Clear All
                </button>
              )}
            </div>

            {/* Active Filters Pills */}
            {hasActiveFilters && (
              <div className="mb-4 pb-4 border-b">
                <p className="text-xs text-gray-500 mb-2">Active Filters:</p>
                <div className="flex flex-wrap gap-2">
                  {selectedCategories.map((cat) => (
                    <button
                      key={cat}
                      onClick={() => onCategoryChange(cat)}
                      className="bg-primary/10 text-primary px-3 py-1 rounded-full text-xs flex items-center gap-1 hover:bg-primary/20 transition"
                    >
                      {cat}
                      <X size={12} />
                    </button>
                  ))}
                  {priceRange < maxPrice && (
                    <button
                      onClick={() => onPriceChange(maxPrice)}
                      className="bg-primary/10 text-primary px-3 py-1 rounded-full text-xs flex items-center gap-1 hover:bg-primary/20 transition"
                    >
                      Under AED {priceRange}
                      <X size={12} />
                    </button>
                  )}
                </div>
              </div>
            )}

            {/* Category Filter - Collapsible */}
            <div className="mb-6">
              <button
                onClick={() => setIsCategoryOpen(!isCategoryOpen)}
                className="w-full flex justify-between items-center mb-3 hover:text-primary transition"
              >
                <h4 className="font-semibold text-sm md:text-base">Category</h4>
                {isCategoryOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
              </button>

              {isCategoryOpen && (
                <div className="space-y-2 animate-fadeIn">
                  {categories.map((cat) => {
                    const count = selectedCategories.includes(cat) ? 1 : 0
                    return (
                      <label
                        key={cat}
                        className="flex items-center justify-between cursor-pointer hover:bg-gray-50 p-2 rounded transition group"
                      >
                        <div className="flex items-center">
                          <input
                            type="checkbox"
                            className="mr-3 w-4 h-4 accent-primary cursor-pointer"
                            checked={selectedCategories.includes(cat)}
                            onChange={() => onCategoryChange(cat)}
                          />
                          <span className="text-xs md:text-sm group-hover:text-primary transition">
                            {cat}
                          </span>
                        </div>
                        {selectedCategories.includes(cat) && (
                          <span className="text-xs text-primary font-semibold">✓</span>
                        )}
                      </label>
                    )
                  })}
                </div>
              )}
            </div>

            {/* Price Range Filter - Collapsible */}
            <div className="mb-6">
              <button
                onClick={() => setIsPriceOpen(!isPriceOpen)}
                className="w-full flex justify-between items-center mb-3 hover:text-primary transition"
              >
                <h4 className="font-semibold text-sm md:text-base">Price Range</h4>
                {isPriceOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
              </button>

              {isPriceOpen && (
                <div className="animate-fadeIn">
                  <input
                    type="range"
                    min="0"
                    max={maxPrice}
                    value={priceRange}
                    onChange={(e) => onPriceChange(Number(e.target.value))}
                    className="w-full accent-primary cursor-pointer"
                  />
                  <div className="flex justify-between text-xs md:text-sm text-gray-600 mt-2">
                    <span>AED 0</span>
                    <span className="font-semibold text-primary">
                      AED {priceRange}
                      {priceRange === maxPrice && '+'}
                    </span>
                  </div>
                  
                  {/* Quick Price Filters */}
                  <div className="mt-3 flex flex-wrap gap-2">
                    {[50, 100, 200, 300].map((price) => (
                      <button
                        key={price}
                        onClick={() => onPriceChange(price)}
                        className={`px-3 py-1 text-xs rounded-full transition ${
                          priceRange === price
                            ? 'bg-primary text-white'
                            : 'bg-gray-100 hover:bg-gray-200'
                        }`}
                      >
                        Under {price}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Apply Filters Button */}
            <button
              onClick={() => {
                onApplyFilters()
                setIsMobileFilterOpen(false)
              }}
              className="w-full bg-primary text-white py-3 rounded-lg hover:bg-blue-700 transition font-semibold text-sm md:text-base shadow-lg"
            >
              Apply Filters
            </button>

            {/* Clear Filters Button - Mobile Only */}
            {hasActiveFilters && (
              <button
                onClick={() => {
                  onClearFilters()
                  setIsMobileFilterOpen(false)
                }}
                className="md:hidden w-full mt-2 border-2 border-gray-300 text-gray-700 py-3 rounded-lg hover:bg-gray-50 transition font-semibold text-sm"
              >
                Clear All Filters
              </button>
            )}
          </div>
        </div>
      </aside>
    </>
  )
}