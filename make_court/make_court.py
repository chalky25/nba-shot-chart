import mplcursors

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc

def draw_court(ax=None, color="blue", lw=0.5, outer_lines=False):
    if ax is None:
        ax = plt.gca()

    # Set black background
    ax.set_facecolor('black')
    
    # Create glow effect by layering lines with decreasing opacity
    glow_colors = ['cyan', '#00ffff80', '#00ffff40', '#00ffff20']
    glow_widths = [lw, lw*2, lw*3, lw*4]
    
    for glow_color, glow_width in zip(glow_colors, glow_widths):
        court_elements = [
            Circle((0, 0), radius=7.5, linewidth=glow_width, color=glow_color, fill=False),
            Rectangle((-30, -12.5), 60, 0, linewidth=glow_width, color=glow_color),
            Rectangle((-80, -47.5), 160, 190, linewidth=glow_width, color=glow_color, fill=False),
            Rectangle((-60, -47.5), 120, 190, linewidth=glow_width, color=glow_color, fill=False),
            Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=glow_width, color=glow_color, fill=False),
            Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=glow_width, color=glow_color),
            Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=glow_width, color=glow_color),
            Rectangle((-220, -47.5), 0, 140, linewidth=glow_width, color=glow_color),
            Rectangle((220, -47.5), 0, 140, linewidth=glow_width, color=glow_color),
            Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=glow_width, color=glow_color),
            Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=glow_width, color=glow_color),
            Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=glow_width, color=glow_color)
        ]
        if outer_lines:
            court_elements.append(Rectangle((-250, -47.5), 500, 470, linewidth=glow_width, color=glow_color, fill=False))
        for element in court_elements:
            ax.add_patch(element)

def shot_chart(data, fg_pct, title="", xlim=(-250, 250), ylim=(422.5, -47.5), line_color="blue",
               court_color="white", court_lw=2, outer_lines=False, flip_court=False, ax=None, show='both'):
    if ax is None:
        ax = plt.gca()
    ax.set_xlim(xlim[::-1] if flip_court else xlim)
    ax.set_ylim(ylim[::-1] if flip_court else ylim)
    ax.tick_params(labelbottom=False, labelleft=False)
    ax.set_title(title, fontsize=14)
    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)
    
    # Define markers and colors for made and missed shots
    x_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
    y_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']

    x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
    y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']
    
    # Create glowing effect for missed shots with multiple layers
    for alpha, size in zip([1.0, 0.5, 0.2], [50, 75, 100]):
        scatter_missed = ax.scatter(x_missed, y_missed,
                                  marker='X',
                                  c='red',
                                  alpha=alpha,
                                  s=size,
                                  linewidths=1,
                                  label='Missed Shot' if alpha == 1.0 else None)
    
    # Create glowing effect for made shots with multiple layers
    for alpha, size in zip([1.0, 0.5, 0.2], [50, 75, 100]):
        scatter_made = ax.scatter(x_made, y_made,
                                marker='o',
                                c='lime',
                                alpha=alpha,
                                s=size,
                                linewidths=1,
                                label='Made Shot' if alpha == 1.0 else None)
    
    mplcursors.cursor(scatter_made, hover=True)
    
    ax.text(0.5, -0.05, f'Season Avg FG%: {fg_pct:.2%}', verticalalignment='center', horizontalalignment='center',
            transform=ax.transAxes, color='black', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
    ax.legend(facecolor='black', labelcolor='white')
    
    return ax