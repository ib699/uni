{{/*
Expand the name of the chart.
*/}}
{{- define "kaas-api.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{/*
Expand the chart name and version.
*/}}
{{- define "kaas-api.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version -}}
{{- end -}}

{{/*
Expand the full name of the chart.
*/}}
{{- define "kaas-api.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Expand the name of the chart and append a suffix.
*/}}
{{- define "kaas-api.fullname.suffix" -}}
{{- printf "%s-%s" (include "kaas-api.fullname" .) .Values.nameSuffix | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "kaas-api.labels" -}}
helm.sh/chart: {{ include "kaas-api.chart" . }}
app.kubernetes.io/name: {{ include "kaas-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

