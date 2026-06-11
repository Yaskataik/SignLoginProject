<template>
  <div class="dashboard-container">
    <aside class="sidebar">
      <div class="brand-logo">
        <h2>Dashboard Portal</h2>
      </div>
      <nav class="nav-menu">
        <button :class="{ active: currentView === 'home' }" @click="currentView = 'home'">
          🏠 Home Packages
        </button>
        <button :class="{ active: currentView === 'buy' }" @click="currentView = 'buy'">
          🛒 Buy Your Package
        </button>
        <button :class="{ active: currentView === 'current' }" @click="currentView = 'current'">
          📊 My Current Package
        </button>
      </nav>
      <button class="logout-btn" @click="handleLogout">Logout</button>
    </aside>

    <main class="main-content">
      <div v-if="currentView === 'home'" class="view-section">
        <h1 class="section-title">Home Packages</h1>
        <p class="subtitle">Choose the perfect internet package that suits your needs.</p>
        
        <div class="packages-grid">
          <div v-for="pkg in packages" :key="pkg.id" class="package-card">
            <span v-if="pkg.popular" class="badge-popular">Popular</span>
            <span class="badge-installation">Free Installation</span>
            <h3>{{ pkg.name }}</h3>
            <p class="speed">{{ pkg.speed }} Mbps</p>
            <p class="purpose">{{ pkg.purpose }}</p>
            <div class="price-tag">KES {{ pkg.price.toLocaleString() }}<span>/month</span></div>
          </div>
        </div>
      </div>

      <div v-if="currentView === 'buy'" class="view-section">
        <h1 class="section-title">Buy Your Package</h1>
        <div class="packages-grid plain-format">
          <div v-for="pkg in packages" :key="pkg.id" class="package-card standard-card">
            <h3>{{ pkg.name }}</h3>
            <p class="speed-large">{{ pkg.speed }} Mbps</p>
            <div class="price-tag">KES {{ pkg.price.toLocaleString() }} / month</div>
            <button class="action-buy-btn" @click="selectAndPurchase(pkg)">
              Activate Plan &rarr;
            </button>
          </div>
        </div>
      </div>

      <div v-if="currentView === 'current'" class="view-section">
        <h1 class="section-title">My Current Package</h1>
        
        <div v-if="userSubscription" class="active-plan-display">
          <div class="plan-summary-banner">
            <h3>Active Subscription: <span class="highlight">{{ userSubscription.name }}</span></h3>
            <p>Speed Tier: <strong>{{ userSubscription.speed }} Mbps</strong></p>
          </div>

          <table class="styled-table">
            <thead>
              <tr>
                <th>Package Name</th>
                <th>Price Paid</th>
                <th>Purchase Date</th>
                <th>Expiry Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{ userSubscription.name }}</td>
                <td>KES {{ userSubscription.price.toLocaleString() }}</td>
                <td>{{ userSubscription.purchaseDate }}</td>
                <td>{{ userSubscription.expiryDate }}</td>
                <td><span class="status-active">Active</span></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="no-plan-message">
          <p>You do not have an active package subscription. Head over to the purchase panel to activate one.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts"> 
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const currentView = ref<string>('home');

// Data Types Interfaces
interface InternetPackage {
  id: number;
  name: string;
  speed: number;
  price: number;
  purpose: string;
  popular?: boolean;
}

interface UserSubscription extends InternetPackage {
  purchaseDate: string;
  expiryDate: string;
}

// Packages Data array mapped directly from your reference sheets
const packages = ref<InternetPackage[]>([
  { id: 1, name: 'Sungura', speed: 10, price: 1499, purpose: 'Built for students' },
  { id: 2, name: 'Chui', speed: 20, price: 1999, purpose: 'For everyday living', popular: true },
  { id: 3, name: 'SimbaMarara', speed: 30, price: 2499, purpose: 'Built for remote workers' },
  { id: 4, name: 'Duma', speed: 90, price: 4999, purpose: 'Full House Speed' }
]);

const userSubscription = ref<UserSubscription | null>(null);

// Simulating data transmission calculation logic
const selectAndPurchase = (selectedPackage: InternetPackage) => {
  const purchase = new Date();
  
  // Calculate expiry milestone (Current date + 30 days time delta)
  const expiry = new Date();
  expiry.setDate(purchase.getDate() + 30);

  // Formatting options for Kenyan system presentations
  const dateOptions: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };

  userSubscription.value = {
    ...selectedPackage,
    purchaseDate: purchase.toLocaleDateString('en-KE', dateOptions),
    expiryDate: expiry.toLocaleDateString('en-KE', dateOptions)
  };

  // Jump tracking view smoothly to represent current status panel
  currentView.value = 'current';
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/');
};
</script>


<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background-color: #121824;
  color: #ffffff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Sidebar Navigation Layout styling */
.sidebar {
  width: 260px;
  background-color: #1a1f2c;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #2e374a;
}
.brand-logo h2 {
  color: #ff7a00;
  font-size: 1.5rem;
  margin-bottom: 2.5rem;
}
.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex-grow: 1;
}
.nav-menu button {
  background: none;
  border: none;
  color: #94a3b8;
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
}
.nav-menu button:hover, .nav-menu button.active {
  background-color: #2e374a;
  color: #ff7a00;
  font-weight: bold;
}
.logout-btn {
  background-color: #b91c1c;
  color: white;
  border: none;
  padding: 0.6rem;
  cursor: pointer;
  border-radius: 4px;
}

/* Main Display Panels styling */
.main-content {
  flex-grow: 1;
  padding: 3rem;
  overflow-y: auto;
}
.section-title {
  font-size: 2.2rem;
  color: #ffffff;
  margin-bottom: 0.5rem;
}
.subtitle {
  color: #94a3b8;
  margin-bottom: 2.5rem;
}
.packages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 2rem;
}

/* Card Presentations */
.package-card {
  background-color: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 2rem;
  position: relative;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.badge-popular {
  position: absolute;
  top: 12px;
  right: 12px;
  background-color: #ff7a00;
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  font-size: 0.75rem;
}
.badge-installation {
  display: inline-block;
  background-color: #10b981;
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}
.price-tag {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ff7a00;
  margin-top: 1.5rem;
}
.price-tag span {
  font-size: 0.9rem;
  color: #94a3b8;
}

/* Interactive Action Buttons */
.action-buy-btn {
  margin-top: 1.5rem;
  width: 100%;
  background-color: #ff7a00;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}
.action-buy-btn:hover {
  background-color: #e66e00;
}

/* Layout Management Data Table styling */
.styled-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1.5rem;
  background-color: #1e293b;
  border-radius: 8px;
  overflow: hidden;
}
.styled-table th {
  background-color: #2e374a;
  color: #ff7a00;
  text-align: left;
  padding: 1rem;
}
.styled-table td {
  padding: 1rem;
  border-bottom: 1px solid #334155;
}
.status-active {
  color: #10b981;
  font-weight: bold;
}
</style>