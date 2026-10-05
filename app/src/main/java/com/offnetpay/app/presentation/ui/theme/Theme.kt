package com.offnetpay.app.presentation.ui.theme

import android.app.Activity
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val NeoPopColorScheme = darkColorScheme(
    primary             = NeoPopColors.Accent,
    onPrimary           = NeoPopColors.Black,
    primaryContainer    = NeoPopColors.AccentDim,
    onPrimaryContainer  = NeoPopColors.Black,
    secondary           = NeoPopColors.TextSecondary,
    onSecondary         = NeoPopColors.Surface,
    background          = NeoPopColors.Black,
    onBackground        = NeoPopColors.TextPrimary,
    surface             = NeoPopColors.Surface,
    onSurface           = NeoPopColors.TextPrimary,
    surfaceVariant      = NeoPopColors.SurfaceHigh,
    onSurfaceVariant    = NeoPopColors.TextSecondary,
    error               = NeoPopColors.Danger,
    onError             = NeoPopColors.Surface,
    outline             = NeoPopColors.Border,
    outlineVariant      = NeoPopColors.BorderStrong
)

/**
 * NeoPOP dark theme — cyber/dark backgrounds, white text, lime green CTA.
 */
@Composable
fun OffNetPayTheme(content: @Composable () -> Unit) {
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = NeoPopColors.Black.toArgb()
            window.navigationBarColor = NeoPopColors.Black.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = false
            WindowCompat.getInsetsController(window, view).isAppearanceLightNavigationBars = false
        }
    }
    MaterialTheme(
        colorScheme = NeoPopColorScheme,
        typography = NeoPopTypography,
        shapes = NeoPopShapes,
        content = content
    )
}
