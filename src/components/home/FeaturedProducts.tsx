'use client'
import Link from 'next/link'
import ProductCard from '@/components/products/ProductCard'
import { products } from '@/data/products'

export default function FeaturedProducts() {
  // Get first 6 products
  const featuredProducts = products.slice(0, 6)

  return (
    <section className="container mx-auto px-4 py-16 bg-gray-50">
      <h2 className="text-3xl font-bold text-center mb-12">Featured Products</h2>
      <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
        {featuredProducts.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
      <div className="text-center mt-12">
        <Link 
          href="/products"
          className="inline-block bg-primary text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold"
        >
          View All Products
        </Link>
      </div>
    </section>
  )
}