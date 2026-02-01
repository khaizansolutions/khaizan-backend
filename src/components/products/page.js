import ProductCard from '@/components/products/ProductCard'

export default function ProductsPage() {
  // Dummy data - will be replaced with API
  const products = Array.from({ length: 12 }, (_, i) => ({
    id: i + 1,
    name: `Product ${i + 1}`,
    price: Math.floor(Math.random() * 200) + 10,
    image: 'https://via.placeholder.com/300',
    category: ['Office Supplies', 'Technology', 'Furniture'][Math.floor(Math.random() * 3)],
  }))

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">All Products</h1>
      
      <div className="flex flex-col md:flex-row gap-8">
        {/* Filters Sidebar */}
        <aside className="w-full md:w-64 shrink-0">
          <div className="bg-white p-4 rounded-lg shadow-md sticky top-24">
            <h3 className="font-bold mb-4">Filters</h3>
            
            <div className="mb-6">
              <h4 className="font-semibold mb-2">Category</h4>
              <div className="space-y-2">
                {['Office Supplies', 'Paper Products', 'Ink & Toner', 'Technology', 'Furniture'].map((cat) => (
                  <label key={cat} className="flex items-center">
                    <input type="checkbox" className="mr-2" />
                    <span className="text-sm">{cat}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="mb-6">
              <h4 className="font-semibold mb-2">Price Range</h4>
              <input type="range" min="0" max="1000" className="w-full" />
              <div className="flex justify-between text-sm text-gray-600">
                <span>AED 0</span>
                <span>AED 1000</span>
              </div>
            </div>

            <button className="w-full bg-primary text-white py-2 rounded-lg hover:bg-blue-700">
              Apply Filters
            </button>
          </div>
        </aside>

        {/* Products Grid */}
        <div className="flex-1">
          <div className="flex justify-between items-center mb-6">
            <p className="text-gray-600">{products.length} Products Found</p>
            <select className="border px-4 py-2 rounded-lg">
              <option>Sort by: Featured</option>
              <option>Price: Low to High</option>
              <option>Price: High to Low</option>
              <option>Newest First</option>
            </select>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}