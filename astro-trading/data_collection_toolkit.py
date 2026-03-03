#!/usr/bin/env python3
"""
Financial Astrology Intelligence Collection Toolkit
Multi-source data gathering for trader account analysis
"""

import requests
import time
import json
import re
from datetime import datetime, timedelta
import os

class FinAstroIntelligence:
    def __init__(self):
        self.targets = {
            't_in_crypto': {'platforms': ['twitter', 'telegram'], 'priority': 1},
            'AstroGann33': {'platforms': ['twitter', 'tradingview'], 'priority': 1}, 
            'starseedastro': {'platforms': ['twitter', 'youtube'], 'priority': 1},
            'PathfinderAstro': {'platforms': ['twitter', 'substack'], 'priority': 1},
            'CrypDoMillions': {'platforms': ['twitter', 'telegram'], 'priority': 1},
        }
        
    def check_wayback_machine(self, username, platform='twitter'):
        """Check archive.org for historical social media data"""
        if platform == 'twitter':
            url = f"https://twitter.com/{username}"
        
        wayback_api = f"http://archive.org/wayback/available?url={url}"
        
        try:
            response = requests.get(wayback_api, timeout=10)
            data = response.json()
            
            if data.get('archived_snapshots', {}).get('closest'):
                snapshot = data['archived_snapshots']['closest']
                return {
                    'available': True,
                    'url': snapshot.get('url'),
                    'timestamp': snapshot.get('timestamp'),
                    'status': snapshot.get('status')
                }
        except Exception as e:
            print(f"Wayback check failed for {username}: {e}")
            
        return {'available': False}
    
    def search_google_cache(self, username, keywords=['bitcoin', 'btc', 'prediction']):
        """Generate Google search queries for cached Twitter content"""
        queries = []
        
        for keyword in keywords:
            # Specific tweet searches
            queries.append(f'site:twitter.com "@{username}" "{keyword}"')
            # Cached page searches  
            queries.append(f'cache:twitter.com/{username} "{keyword}"')
            # Date-specific searches
            for year in ['2023', '2024', '2025']:
                queries.append(f'site:twitter.com "@{username}" "{keyword}" "{year}"')
        
        return queries
    
    def find_cross_platform_presence(self, username):
        """Discover other platforms where this user might be active"""
        platforms_to_check = {
            'youtube': f"https://www.youtube.com/@{username}",
            'telegram': f"https://t.me/{username}", 
            'medium': f"https://medium.com/@{username}",
            'substack': f"https://{username}.substack.com",
            'tradingview': f"https://www.tradingview.com/u/{username}",
        }
        
        found_platforms = []
        
        for platform, url in platforms_to_check.items():
            try:
                # Quick HEAD request to check if profile exists
                response = requests.head(url, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    found_platforms.append({
                        'platform': platform,
                        'url': url,
                        'status': 'active'
                    })
            except:
                continue
                
        return found_platforms
    
    def extract_telegram_channel_info(self, channel_name):
        """Get public Telegram channel information"""
        # For public channels only - no authentication required
        telegram_url = f"https://t.me/s/{channel_name}"  # Public channel preview
        
        try:
            response = requests.get(telegram_url, timeout=10)
            if response.status_code == 200:
                # Basic info extraction from public preview
                content = response.text
                
                # Extract channel title, description, member count
                title_match = re.search(r'<meta property="og:title" content="([^"]+)"', content)
                desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', content)
                
                return {
                    'url': telegram_url,
                    'title': title_match.group(1) if title_match else None,
                    'description': desc_match.group(1) if desc_match else None,
                    'accessible': True
                }
        except Exception as e:
            print(f"Telegram check failed for {channel_name}: {e}")
            
        return {'accessible': False}
    
    def scan_all_targets(self):
        """Comprehensive intelligence scan of all targets"""
        results = {}
        
        print("FINANCIAL ASTROLOGY INTELLIGENCE SCAN")
        print("="*45)
        
        for username, info in self.targets.items():
            print(f"\n📡 Scanning: @{username} (Priority {info['priority']})")
            
            target_results = {
                'username': username,
                'priority': info['priority'],
                'wayback_available': False,
                'cross_platforms': [],
                'google_queries': [],
                'telegram_info': None
            }
            
            # Check Wayback Machine
            wayback = self.check_wayback_machine(username)
            if wayback['available']:
                print(f"  ✅ Wayback: {wayback['timestamp']} - {wayback['url']}")
                target_results['wayback_available'] = wayback
            else:
                print(f"  ❌ Wayback: No archives found")
            
            # Find cross-platform presence
            platforms = self.find_cross_platform_presence(username)
            if platforms:
                print(f"  🔍 Cross-platform presence:")
                for platform in platforms:
                    print(f"    • {platform['platform']}: {platform['url']}")
                target_results['cross_platforms'] = platforms
            
            # Generate Google search queries
            queries = self.search_google_cache(username)
            target_results['google_queries'] = queries[:5]  # Top 5 queries
            
            # Check Telegram if relevant  
            if 'telegram' in info['platforms']:
                tg_info = self.extract_telegram_channel_info(username)
                if tg_info['accessible']:
                    print(f"  📱 Telegram: {tg_info['title']}")
                    target_results['telegram_info'] = tg_info
            
            results[username] = target_results
            time.sleep(2)  # Be respectful with requests
            
        return results
    
    def generate_collection_plan(self, scan_results):
        """Generate prioritized data collection plan"""
        print(f"\n📋 COLLECTION STRATEGY RECOMMENDATIONS")
        print("="*45)
        
        high_value_targets = []
        
        for username, data in scan_results.items():
            score = 0
            methods = []
            
            # Score based on data availability
            if data['wayback_available']:
                score += 10
                methods.append("Wayback Machine extraction")
                
            if data['cross_platforms']:
                score += len(data['cross_platforms']) * 3
                for platform in data['cross_platforms']:
                    methods.append(f"{platform['platform'].title()} scraping")
                    
            if data['telegram_info'] and data['telegram_info']['accessible']:
                score += 8
                methods.append("Telegram channel monitoring")
            
            # Priority bonus
            score += (4 - data['priority']) * 5
            
            high_value_targets.append({
                'username': username,
                'score': score,
                'methods': methods,
                'priority': data['priority']
            })
        
        # Sort by score
        high_value_targets.sort(key=lambda x: x['score'], reverse=True)
        
        print("\n🎯 TOP COLLECTION TARGETS:")
        for i, target in enumerate(high_value_targets[:5], 1):
            print(f"\n{i}. @{target['username']} (Score: {target['score']})")
            for method in target['methods']:
                print(f"   • {method}")
        
        return high_value_targets
    
    def export_google_queries(self, scan_results, output_file='google_queries.txt'):
        """Export all Google search queries for manual execution"""
        all_queries = []
        
        for username, data in scan_results.items():
            all_queries.extend([f"# {username}"] + data['google_queries'] + [''])
        
        with open(output_file, 'w') as f:
            f.write('\n'.join(all_queries))
            
        print(f"\n💾 Google queries exported to: {output_file}")
        print("   Execute these manually to find cached content")


def main():
    """Run the intelligence collection scan"""
    intel = FinAstroIntelligence()
    
    # Run comprehensive scan
    results = intel.scan_all_targets()
    
    # Generate collection strategy
    targets = intel.generate_collection_plan(results)
    
    # Export Google queries for manual search
    intel.export_google_queries(results)
    
    # Save full results
    with open('intelligence_scan_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Full results saved to: intelligence_scan_results.json")
    
    return results

if __name__ == "__main__":
    main()