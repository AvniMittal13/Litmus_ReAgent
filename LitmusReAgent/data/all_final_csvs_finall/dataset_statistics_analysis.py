"""
Comprehensive Dataset Statistics Analysis for Combined and Reduced CSVs
Generates detailed statistics, comparisons, and academic-quality visualizations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
import numpy as np
from collections import defaultdict
import importlib.util
import sys

# Set style for academic publications
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 16
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14

# Task mapping
TASK_FOLDERS = {
    "01_Code_Generation": "Code Generation",
    "02_Math_Reasoning": "Math Reasoning",
    "03_QA_VQA": "QA/VQA",
    "04_Classification_NLI": "Classification/NLI",
    "05_Text_Summarization": "Text Summarization",
    "06_Machine_Translation": "Machine Translation"
}


class DatasetStatisticsAnalyzer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.statistics = {}
        self.output_dir = self.base_path / "statistics_output"
        self.output_dir.mkdir(exist_ok=True)
        
    def load_mapping_file(self, mapping_file_path):
        """DEPRECATED: Load a language-models mapping file. Use parse_csv_directly instead."""
        return None
    
    def parse_csv_directly(self, csv_file_path):
        """Parse CSV file directly to extract unique languages and models from the data."""
        try:
            df = pd.read_csv(csv_file_path)
            
            # Extract unique languages
            unique_languages = set()
            for languages_str in df['Languages'].dropna():
                langs = [lang.strip() for lang in str(languages_str).split(',')]
                unique_languages.update(langs)
            
            # Extract unique models
            unique_models = set()
            for models_str in df['Models'].dropna():
                models = [model.strip() for model in str(models_str).split(',')]
                unique_models.update(models)
            
            # Build language_counts (each language appears with at least 1 model)
            language_counts = {lang: 1 for lang in unique_languages}
            
            return {
                'unique_languages': len(unique_languages),
                'unique_models': len(unique_models),
                'languages_list': sorted(unique_languages),
                'models_list': sorted(unique_models),
                'language_counts': language_counts
            }
            
        except Exception as e:
            print(f"    Error parsing CSV file {csv_file_path}: {e}")
            return None
    
    def analyze_csv(self, csv_path):
        """Analyze a single CSV file and return statistics."""
        try:
            df = pd.read_csv(csv_path)
            
            stats = {
                'total_papers': len(df),
                'unique_languages': df['Language'].nunique() if 'Language' in df.columns else 0,
                'unique_models': df['Model'].nunique() if 'Model' in df.columns else 0,
                'languages_list': sorted(df['Language'].unique().tolist()) if 'Language' in df.columns else [],
                'models_list': sorted(df['Model'].unique().tolist()) if 'Model' in df.columns else [],
                'language_counts': df['Language'].value_counts().to_dict() if 'Language' in df.columns else {},
                'model_counts': df['Model'].value_counts().to_dict() if 'Model' in df.columns else {},
                'columns': df.columns.tolist(),
                'shape': df.shape
            }
            
            # Additional metrics
            if 'Year' in df.columns:
                stats['year_range'] = (int(df['Year'].min()), int(df['Year'].max()))
                stats['papers_per_year'] = df['Year'].value_counts().sort_index().to_dict()
            
            if 'Venue' in df.columns:
                stats['unique_venues'] = df['Venue'].nunique()
                stats['top_venues'] = df['Venue'].value_counts().head(5).to_dict()
            
            return stats
        except Exception as e:
            print(f"Error analyzing {csv_path}: {e}")
            return None
    
    def collect_task_statistics(self):
        """Collect statistics for all tasks by parsing CSV files directly."""
        for task_folder, task_name in TASK_FOLDERS.items():
            task_path = self.base_path / task_folder
            if not task_path.exists():
                print(f"Warning: {task_folder} not found")
                continue
            
            print(f"\nAnalyzing {task_name}...")
            
            # Find CSV files
            combined_csv = task_path / f"combined_{task_folder.lower()}.csv"
            reduced_csv = task_path / f"reduced_combined_{task_folder.lower()}.csv"
            
            task_stats = {
                'task_name': task_name,
                'task_folder': task_folder,
                'combined': None,
                'reduced': None,
                'comparison': {}
            }
            
            # Get combined statistics by parsing CSV directly
            if combined_csv.exists():
                print(f"  Parsing combined CSV...")
                combined_stats = self.parse_csv_directly(combined_csv)
                if combined_stats:
                    # Add paper count
                    try:
                        df = pd.read_csv(combined_csv)
                        combined_stats['total_papers'] = len(df)
                        task_stats['combined'] = combined_stats
                    except Exception as e:
                        print(f"    Error reading CSV: {e}")
            else:
                print(f"  Warning: Combined CSV not found at {combined_csv}")
            
            # Get reduced statistics by parsing CSV directly
            if reduced_csv.exists():
                print(f"  Parsing reduced CSV...")
                reduced_stats = self.parse_csv_directly(reduced_csv)
                if reduced_stats:
                    # Add paper count
                    try:
                        df = pd.read_csv(reduced_csv)
                        reduced_stats['total_papers'] = len(df)
                        task_stats['reduced'] = reduced_stats
                    except Exception as e:
                        print(f"    Error reading CSV: {e}")
            else:
                print(f"  Warning: Reduced CSV not found at {reduced_csv}")
            
            # Compute comparison metrics
            if task_stats['combined'] and task_stats['reduced']:
                combined = task_stats['combined']
                reduced = task_stats['reduced']
                
                task_stats['comparison'] = {
                    'papers_reduction': combined['total_papers'] - reduced['total_papers'],
                    'papers_reduction_pct': ((combined['total_papers'] - reduced['total_papers']) / combined['total_papers'] * 100) if combined['total_papers'] > 0 else 0,
                    'languages_reduction': combined['unique_languages'] - reduced['unique_languages'],
                    'languages_reduction_pct': ((combined['unique_languages'] - reduced['unique_languages']) / combined['unique_languages'] * 100) if combined['unique_languages'] > 0 else 0,
                    'models_reduction': combined['unique_models'] - reduced['unique_models'],
                    'models_reduction_pct': ((combined['unique_models'] - reduced['unique_models']) / combined['unique_models'] * 100) if combined['unique_models'] > 0 else 0,
                    'languages_only_in_combined': list(set(combined['languages_list']) - set(reduced['languages_list'])),
                    'models_only_in_combined': list(set(combined['models_list']) - set(reduced['models_list']))
                }
            
            self.statistics[task_folder] = task_stats
            print(f"  ✓ Completed analysis for {task_name}")

    
    def generate_summary_table(self):
        """Generate summary table comparing combined vs reduced datasets."""
        print("\n" + "="*100)
        print("DATASET STATISTICS SUMMARY")
        print("="*100)
        
        summary_data = []
        
        for task_folder in TASK_FOLDERS.keys():
            if task_folder not in self.statistics:
                continue
            
            stats = self.statistics[task_folder]
            task_name = stats['task_name']
            
            row = {'Task': task_name}
            
            if stats['combined']:
                row['Combined_Papers'] = stats['combined']['total_papers']
                row['Combined_Languages'] = stats['combined']['unique_languages']
                row['Combined_Models'] = stats['combined']['unique_models']
            else:
                row['Combined_Papers'] = 0
                row['Combined_Languages'] = 0
                row['Combined_Models'] = 0
            
            if stats['reduced']:
                row['Reduced_Papers'] = stats['reduced']['total_papers']
                row['Reduced_Languages'] = stats['reduced']['unique_languages']
                row['Reduced_Models'] = stats['reduced']['unique_models']
            else:
                row['Reduced_Papers'] = 0
                row['Reduced_Languages'] = 0
                row['Reduced_Models'] = 0
            
            if stats['comparison']:
                row['Papers_Reduction_%'] = f"{stats['comparison']['papers_reduction_pct']:.1f}"
                row['Languages_Reduction_%'] = f"{stats['comparison']['languages_reduction_pct']:.1f}"
                row['Models_Reduction_%'] = f"{stats['comparison']['models_reduction_pct']:.1f}"
            else:
                row['Papers_Reduction_%'] = "N/A"
                row['Languages_Reduction_%'] = "N/A"
                row['Models_Reduction_%'] = "N/A"
            
            summary_data.append(row)
        
        # Create DataFrame and display
        df_summary = pd.DataFrame(summary_data)
        
        # Save to CSV
        summary_file = self.output_dir / "dataset_summary_table.csv"
        df_summary.to_csv(summary_file, index=False)
        print(f"\n✓ Summary table saved to: {summary_file}")
        
        # Display formatted table
        print("\n" + df_summary.to_string(index=False))
        print("="*100)
        
        return df_summary
    
    def generate_detailed_report(self):
        """Generate detailed JSON report with all statistics."""
        report_file = self.output_dir / "detailed_statistics_report.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.statistics, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Detailed report saved to: {report_file}")
    
    def visualize_papers_comparison(self):
        """Generate bar chart comparing paper counts."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        tasks = []
        combined_counts = []
        reduced_counts = []
        
        for task_folder in TASK_FOLDERS.keys():
            if task_folder not in self.statistics:
                continue
            
            stats = self.statistics[task_folder]
            tasks.append(stats['task_name'])
            
            combined_counts.append(stats['combined']['total_papers'] if stats['combined'] else 0)
            reduced_counts.append(stats['reduced']['total_papers'] if stats['reduced'] else 0)
        
        x = np.arange(len(tasks))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, combined_counts, width, label='Combined', alpha=0.8)
        bars2 = ax.bar(x + width/2, reduced_counts, width, label='Reduced', alpha=0.8)
        
        ax.set_xlabel('Task')
        ax.set_ylabel('Number of Papers')
        ax.set_title('Paper Count Comparison: Combined vs Reduced Datasets')
        ax.set_xticks(x)
        ax.set_xticklabels(tasks, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=12)
        
        plt.tight_layout()
        output_file = self.output_dir / "papers_comparison.png"
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
        print(f"✓ Visualization saved: {output_file}")
    
    def visualize_languages_comparison(self):
        """Generate bar chart comparing language counts."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        tasks = []
        combined_counts = []
        reduced_counts = []
        
        for task_folder in TASK_FOLDERS.keys():
            if task_folder not in self.statistics:
                continue
            
            stats = self.statistics[task_folder]
            tasks.append(stats['task_name'])
            
            combined_counts.append(stats['combined']['unique_languages'] if stats['combined'] else 0)
            reduced_counts.append(stats['reduced']['unique_languages'] if stats['reduced'] else 0)
        
        x = np.arange(len(tasks))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, combined_counts, width, label='Combined', alpha=0.8, color='#1f77b4')
        bars2 = ax.bar(x + width/2, reduced_counts, width, label='Reduced', alpha=0.8, color='#ff7f0e')
        
        ax.set_xlabel('Task')
        ax.set_ylabel('Number of Languages')
        ax.set_title('Language Coverage Comparison: Combined vs Reduced Datasets')
        ax.set_xticks(x)
        ax.set_xticklabels(tasks, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=12)
        
        plt.tight_layout()
        output_file = self.output_dir / "languages_comparison.png"
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
        print(f"✓ Visualization saved: {output_file}")
    
    def visualize_models_comparison(self):
        """Generate bar chart comparing model counts."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        tasks = []
        combined_counts = []
        reduced_counts = []
        
        for task_folder in TASK_FOLDERS.keys():
            if task_folder not in self.statistics:
                continue
            
            stats = self.statistics[task_folder]
            tasks.append(stats['task_name'])
            
            combined_counts.append(stats['combined']['unique_models'] if stats['combined'] else 0)
            reduced_counts.append(stats['reduced']['unique_models'] if stats['reduced'] else 0)
        
        x = np.arange(len(tasks))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, combined_counts, width, label='Combined', alpha=0.8, color='#2ca02c')
        bars2 = ax.bar(x + width/2, reduced_counts, width, label='Reduced', alpha=0.8, color='#d62728')
        
        ax.set_xlabel('Task')
        ax.set_ylabel('Number of Models')
        ax.set_title('Model Coverage Comparison: Combined vs Reduced Datasets')
        ax.set_xticks(x)
        ax.set_xticklabels(tasks, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=12)
        
        plt.tight_layout()
        output_file = self.output_dir / "models_comparison.png"
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
        print(f"✓ Visualization saved: {output_file}")
    
    def visualize_reduction_percentages(self):
        """Generate stacked bar chart showing reduction percentages."""
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        tasks = []
        papers_red = []
        langs_red = []
        models_red = []
        
        for task_folder in TASK_FOLDERS.keys():
            if task_folder not in self.statistics:
                continue
            
            stats = self.statistics[task_folder]
            if not stats['comparison']:
                continue
            
            tasks.append(stats['task_name'])
            papers_red.append(stats['comparison']['papers_reduction_pct'])
            langs_red.append(stats['comparison']['languages_reduction_pct'])
            models_red.append(stats['comparison']['models_reduction_pct'])
        
        # Papers reduction
        ax1.barh(tasks, papers_red, color='#1f77b4', alpha=0.7)
        ax1.set_xlabel('Reduction (%)')
        ax1.set_title('Papers Reduction')
        ax1.grid(axis='x', alpha=0.3)
        for i, v in enumerate(papers_red):
            ax1.text(v + 1, i, f'{v:.1f}%', va='center', fontsize=12)
        
        # Languages reduction
        ax2.barh(tasks, langs_red, color='#ff7f0e', alpha=0.7)
        ax2.set_xlabel('Reduction (%)')
        ax2.set_title('Languages Reduction')
        ax2.grid(axis='x', alpha=0.3)
        for i, v in enumerate(langs_red):
            ax2.text(v + 1, i, f'{v:.1f}%', va='center', fontsize=12)
        
        # Models reduction
        ax3.barh(tasks, models_red, color='#2ca02c', alpha=0.7)
        ax3.set_xlabel('Reduction (%)')
        ax3.set_title('Models Reduction')
        ax3.grid(axis='x', alpha=0.3)
        for i, v in enumerate(models_red):
            ax3.text(v + 1, i, f'{v:.1f}%', va='center', fontsize=12)
        
        plt.suptitle('Reduction Percentages: Combined to Reduced', fontsize=18, y=1.02)
        plt.tight_layout()
        output_file = self.output_dir / "reduction_percentages.png"
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
        print(f"✓ Visualization saved: {output_file}")
    
    def visualize_language_distribution_per_task(self):
        """Generate detailed language distribution charts for each task."""
        for task_folder in TASK_FOLDERS.keys():
            if task_folder not in self.statistics:
                continue
            
            stats = self.statistics[task_folder]
            if not stats['combined'] or not stats['reduced']:
                continue
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
            
            # Combined dataset
            if stats['combined']['language_counts']:
                lang_counts = stats['combined']['language_counts']
                top_langs = dict(sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:15])
                
                ax1.barh(list(top_langs.keys()), list(top_langs.values()), alpha=0.7, color='#1f77b4')
                ax1.set_xlabel('Number of Papers')
                ax1.set_title(f'Combined Dataset - Top 15 Languages')
                ax1.grid(axis='x', alpha=0.3)
                ax1.invert_yaxis()
            
            # Reduced dataset
            if stats['reduced']['language_counts']:
                lang_counts = stats['reduced']['language_counts']
                top_langs = dict(sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:15])
                
                ax2.barh(list(top_langs.keys()), list(top_langs.values()), alpha=0.7, color='#ff7f0e')
                ax2.set_xlabel('Number of Papers')
                ax2.set_title(f'Reduced Dataset - Top 15 Languages')
                ax2.grid(axis='x', alpha=0.3)
                ax2.invert_yaxis()
            
            plt.suptitle(f'{stats["task_name"]} - Language Distribution', fontsize=18, y=1.02)
            plt.tight_layout()
            output_file = self.output_dir / f"language_distribution_{task_folder}.png"
            plt.savefig(output_file, bbox_inches='tight')
            plt.close()
            print(f"✓ Visualization saved: {output_file}")
    
    def visualize_overall_statistics(self):
        """Generate overall aggregate statistics visualization."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # Total papers across all tasks
        total_combined = sum(s['combined']['total_papers'] for s in self.statistics.values() if s['combined'])
        total_reduced = sum(s['reduced']['total_papers'] for s in self.statistics.values() if s['reduced'])
        
        ax1.bar(['Combined', 'Reduced'], [total_combined, total_reduced], color=['#1f77b4', '#ff7f0e'], alpha=0.7)
        ax1.set_ylabel('Total Papers')
        ax1.set_title('Total Papers Across All Tasks')
        ax1.grid(axis='y', alpha=0.3)
        for i, v in enumerate([total_combined, total_reduced]):
            ax1.text(i, v, f'{v}', ha='center', va='bottom', fontsize=14, fontweight='bold')
        
        # Total unique languages
        all_combined_langs = set()
        all_reduced_langs = set()
        for stats in self.statistics.values():
            if stats['combined']:
                all_combined_langs.update(stats['combined']['languages_list'])
            if stats['reduced']:
                all_reduced_langs.update(stats['reduced']['languages_list'])
        
        ax2.bar(['Combined', 'Reduced'], [len(all_combined_langs), len(all_reduced_langs)], 
                color=['#2ca02c', '#d62728'], alpha=0.7)
        ax2.set_ylabel('Unique Languages')
        ax2.set_title('Total Unique Languages Across All Tasks')
        ax2.grid(axis='y', alpha=0.3)
        for i, v in enumerate([len(all_combined_langs), len(all_reduced_langs)]):
            ax2.text(i, v, f'{v}', ha='center', va='bottom', fontsize=14, fontweight='bold')
        
        # Total unique models
        all_combined_models = set()
        all_reduced_models = set()
        for stats in self.statistics.values():
            if stats['combined']:
                all_combined_models.update(stats['combined']['models_list'])
            if stats['reduced']:
                all_reduced_models.update(stats['reduced']['models_list'])
        
        ax3.bar(['Combined', 'Reduced'], [len(all_combined_models), len(all_reduced_models)], 
                color=['#9467bd', '#8c564b'], alpha=0.7)
        ax3.set_ylabel('Unique Models')
        ax3.set_title('Total Unique Models Across All Tasks')
        ax3.grid(axis='y', alpha=0.3)
        for i, v in enumerate([len(all_combined_models), len(all_reduced_models)]):
            ax3.text(i, v, f'{v}', ha='center', va='bottom', fontsize=14, fontweight='bold')
        
        # Average reduction percentages
        avg_paper_red = np.mean([s['comparison']['papers_reduction_pct'] for s in self.statistics.values() if s['comparison']])
        avg_lang_red = np.mean([s['comparison']['languages_reduction_pct'] for s in self.statistics.values() if s['comparison']])
        avg_model_red = np.mean([s['comparison']['models_reduction_pct'] for s in self.statistics.values() if s['comparison']])
        
        categories = ['Papers', 'Languages', 'Models']
        reductions = [avg_paper_red, avg_lang_red, avg_model_red]
        
        ax4.bar(categories, reductions, color=['#1f77b4', '#ff7f0e', '#2ca02c'], alpha=0.7)
        ax4.set_ylabel('Reduction Percentage (%)')
        ax4.set_title('Average Reduction Percentages')
        ax4.grid(axis='y', alpha=0.3)
        for i, v in enumerate(reductions):
            ax4.text(i, v, f'{v:.1f}%', ha='center', va='bottom', fontsize=14, fontweight='bold')
        
        plt.suptitle('Overall Dataset Statistics Summary', fontsize=20, y=1.00)
        plt.tight_layout()
        output_file = self.output_dir / "overall_statistics.png"
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
        print(f"✓ Visualization saved: {output_file}")
    
    def generate_latex_table(self):
        """Generate LaTeX table for academic papers."""
        latex_lines = []
        latex_lines.append("\\begin{table}[htbp]")
        latex_lines.append("\\centering")
        latex_lines.append("\\caption{Dataset Statistics: Combined vs Reduced}")
        latex_lines.append("\\label{tab:dataset_stats}")
        latex_lines.append("\\begin{tabular}{lrrrrrr}")
        latex_lines.append("\\hline")
        latex_lines.append("\\textbf{Task} & \\multicolumn{3}{c}{\\textbf{Combined}} & \\multicolumn{3}{c}{\\textbf{Reduced}} \\\\")
        latex_lines.append(" & Papers & Langs & Models & Papers & Langs & Models \\\\")
        latex_lines.append("\\hline")
        
        for task_folder in TASK_FOLDERS.keys():
            if task_folder not in self.statistics:
                continue
            
            stats = self.statistics[task_folder]
            task_name = stats['task_name'].replace('&', '\\&')
            
            comb_papers = stats['combined']['total_papers'] if stats['combined'] else 0
            comb_langs = stats['combined']['unique_languages'] if stats['combined'] else 0
            comb_models = stats['combined']['unique_models'] if stats['combined'] else 0
            
            red_papers = stats['reduced']['total_papers'] if stats['reduced'] else 0
            red_langs = stats['reduced']['unique_languages'] if stats['reduced'] else 0
            red_models = stats['reduced']['unique_models'] if stats['reduced'] else 0
            
            latex_lines.append(f"{task_name} & {comb_papers} & {comb_langs} & {comb_models} & {red_papers} & {red_langs} & {red_models} \\\\")
        
        latex_lines.append("\\hline")
        latex_lines.append("\\end{tabular}")
        latex_lines.append("\\end{table}")
        
        latex_file = self.output_dir / "dataset_statistics_table.tex"
        with open(latex_file, 'w') as f:
            f.write('\n'.join(latex_lines))
        
        print(f"✓ LaTeX table saved: {latex_file}")
    
    def run_complete_analysis(self):
        """Run complete analysis pipeline."""
        print("\n" + "="*100)
        print("STARTING COMPREHENSIVE DATASET STATISTICS ANALYSIS")
        print("="*100)
        
        # Collect statistics
        self.collect_task_statistics()
        
        # Generate summary table
        self.generate_summary_table()
        
        # Generate detailed report
        self.generate_detailed_report()
        
        # Generate all visualizations
        print("\n" + "="*100)
        print("GENERATING VISUALIZATIONS")
        print("="*100)
        
        self.visualize_papers_comparison()
        self.visualize_languages_comparison()
        self.visualize_models_comparison()
        self.visualize_reduction_percentages()
        self.visualize_overall_statistics()
        
        # Generate LaTeX table
        print("\n" + "="*100)
        print("GENERATING LATEX TABLE")
        print("="*100)
        self.generate_latex_table()
        
        print("\n" + "="*100)
        print("ANALYSIS COMPLETE!")
        print(f"All outputs saved to: {self.output_dir}")
        print("="*100)


if __name__ == "__main__":
    base_path = Path(__file__).parent
    analyzer = DatasetStatisticsAnalyzer(base_path)
    analyzer.run_complete_analysis()
