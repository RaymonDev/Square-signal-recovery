import numpy as np
import os
import matplotlib.pyplot as plt

amplitude = 1.0
phase = 0.0
period = 1.0


def points_list(round_points, round_points_loc):
    
    #dictionary to store the points
    point_dict = dict(zip(round_points_loc, round_points))

    point_listing = []
    
    
    #unique values of round_points
    round_points_unique = list(set(round_points))
    print(f'Round Points Unique: {round_points_unique}')
    
    print("Biggest value of round_points_unique: ", max(round_points_unique))
    print("Smallest value of round_points_unique: ", min(round_points_unique))
    
    print("-"*20)
    
    #store in point_listing points with duplicated key in groups of two but the values have to be inverse
    
    for key, value in point_dict.items():
        if value == 0:
            point_listing.append((key, value))
            point_listing.append((key, max(round_points_unique)))
        else:
            point_listing.append((key, value))
            point_listing.append((key, min(round_points_unique)))
    
    #sort the point_listing by the first element of the tuple
    point_listing = sorted(point_listing, key=lambda x: x[0])
    
    print(f'Point Listing: {point_listing}')
    print("-"*20)
    
    return point_listing





def squared_signal():
    # Generate time values for one second
    t = np.linspace(0, 2, 2000)

    # Define the variables for amplitude, phase, and period

    # Generate squared signal values
    signal = amplitude * np.sign(np.sin(2 * np.pi * t / period + phase))
    
    # Set negative values to zero
    signal[signal < 0] = 0

    # Add noise to the amplitude
    noise = np.random.normal(0, 0.1, len(signal))
    signal_with_noise = signal + noise
    
    return signal_with_noise


def adaptive_filter(signal):
    
    # derivative of the signal
    derivative_signal = np.diff(signal)
    
    # Get points over 0.5 and under -0.5
    points_over = np.where(derivative_signal > 0.70)[0]
    points_under = np.where(derivative_signal < -0.70)[0]
    
    round_points = []
    round_points_loc = []
    
    for point_over in points_over:
        round_points.append(round(derivative_signal[point_over]))
        round_points_loc.append(point_over)
    
    for point_under in points_under:
        if round(derivative_signal[point_under]) < 0:
            pointvalue = 0
        
        round_points.append(pointvalue)
        round_points_loc.append(point_under)
        
    print("-"*20)    
    print(f'Round Points: {round_points}')
    print(f'Round Points Loc: {round_points_loc}')
    print("-"*20)
        
    points = points_list(round_points, round_points_loc)
    
    manager = plt.get_current_fig_manager()

    # Set the window title
    manager.set_window_title("Recovery of the original signal")
    
    # Original plot
    plt.subplot(1, 3, 1)
    plt.plot(signal, label='Original Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Original signal')
    plt.legend()
    plt.grid(True)
    
    # Filtered plot
    plt.subplot(1, 3, 2)
    plt.plot(derivative_signal, label='Derivative Signal')
    
    plt.scatter(points_over, derivative_signal[points_over], color='red', label='Points Over')
    plt.scatter(points_under, derivative_signal[points_under], color='blue', label='Points Under')
    
    plt.title('Derivative Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    
    # Recovered plot
    plt.subplot(1, 3, 3)
    
    x, y = zip(*points)
    
    # Draw a vertical line for points with same x
    for i in range(0, len(x), 2):
        plt.plot([x[i+1], x[i+1]], [y[i], y[i+1]], color='red')
        
    x_unique = list(set(x))
    
    # Draw a horizontal line for points with same y and close values of x and Y = 1 or Y = 0
    for i in range(0, len(x_unique)+2, 2):
        plt.plot([x[i], x[i+3]], [y[i], y[i+3]], color='blue')
    
    
    plt.title('Recovered Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.show()


if __name__ == '__main__':
    signal = squared_signal()
    adaptive_filter(signal)
